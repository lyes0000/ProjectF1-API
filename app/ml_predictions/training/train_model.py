"""
Model training script
Correct formulation: predict race winner probability
"""

import os
import joblib
import pandas as pd
from datetime import datetime

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, log_loss

from races.models import Race
from ml_predictions.features.feature_builder import FeatureBuilder


class ModelTrainer:
    """
    Handles ML model training and evaluation
    Predicts win probability (binary classification)
    """

    def __init__(self, model_version="random_forest_v1"):
        self.model_version = model_version
        self.model = None
        self.feature_builder = FeatureBuilder()
        self.feature_names = self.feature_builder.get_feature_names()

    def prepare_data(self, year_start=2019, year_end=2024):
        """
        Prepare training data from historical races
        """
        print(f"Loading races from {year_start} to {year_end}")

        races = Race.objects.filter(
            year__gte=year_start,
            year__lte=year_end
        ).order_by("year", "round")

        print(f"Found {races.count()} races")

        print("Building features...")
        dataset = self.feature_builder.build_training_dataset(races)

        # Add race date (required for time-based split)
        race_dates = {
            race.id: race.date
            for race in races
        }
        dataset["race_date"] = dataset["race_id"].map(race_dates)

        # Target: winner (binary)
        dataset["is_winner"] = (dataset["position"] == 1).astype(int)

        # Features / target
        X = dataset[self.feature_names]
        y = dataset["is_winner"]

        # Handle missing values
        X = X.fillna(X.mean())

        print(f"Dataset size: {len(dataset)} samples")
        print(f"Winner rate: {y.mean():.2%}")

        return X, y, dataset

    def train(self, X, y, dataset=None):
        """
        Train model using time-based split
        """
        if dataset is None:
            raise ValueError("Dataset is required for time-based split")

        print("\nSplitting data by time (no leakage)...")

        cutoff_date = dataset["race_date"].quantile(0.8)

        train_idx = dataset["race_date"] < cutoff_date
        test_idx = dataset["race_date"] >= cutoff_date

        X_train, X_test = X.loc[train_idx], X.loc[test_idx]
        y_train, y_test = y.loc[train_idx], y.loc[test_idx]

        print(f"Training samples: {len(X_train)}")
        print(f"Test samples: {len(X_test)}")

        print("\nTraining Random Forest model...")

        self.model = RandomForestClassifier(
            n_estimators=300,
            max_depth=8,
            min_samples_split=5,
            class_weight="balanced",
            random_state=42,
            n_jobs=-1
        )

        self.model.fit(X_train, y_train)
        print("✓ Training complete")

        print("\nEvaluating model...")

        train_probs = self.model.predict_proba(X_train)[:, 1]
        test_probs = self.model.predict_proba(X_test)[:, 1]

        metrics = {
            "train_auc": roc_auc_score(y_train, train_probs),
            "test_auc": roc_auc_score(y_test, test_probs),
            "test_log_loss": log_loss(y_test, test_probs),
            "top_3_accuracy": self._top_k_accuracy(
                dataset.loc[test_idx],
                test_probs,
                k=3
            ),
            "top_5_accuracy": self._top_k_accuracy(
                dataset.loc[test_idx],
                test_probs,
                k=5
            ),
        }

        print("\nEvaluation results:")
        for k, v in metrics.items():
            print(f"{k}: {v:.3f}")

        # Feature importance
        feature_importance = pd.DataFrame({
            "feature": self.feature_names,
            "importance": self.model.feature_importances_
        }).sort_values("importance", ascending=False)

        print("\nFeature importance:")
        print(feature_importance)

        metrics["feature_importance"] = feature_importance.to_dict("records")

        return self.model, metrics

    def _top_k_accuracy(self, dataset, probs, k=3):
        """
        Race-level Top-K accuracy:
        Was the real winner in the top K predictions?
        """
        df = dataset.copy()
        df["prob"] = probs

        correct = 0
        total = df["race_id"].nunique()

        for _, group in df.groupby("race_id"):
            top_k = group.sort_values("prob", ascending=False).head(k)
            if top_k["is_winner"].any():
                correct += 1

        return correct / total if total > 0 else 0

    def save_model(self, model_dir="ml_predictions/ml_models"):
        """
        Save trained model to disk
        """
        if self.model is None:
            raise ValueError("No model to save")

        os.makedirs(model_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.model_version}_{timestamp}.joblib"
        filepath = os.path.join(model_dir, filename)

        payload = {
            "model": self.model,
            "feature_names": self.feature_names,
            "version": self.model_version,
            "trained_at": timestamp,
        }

        joblib.dump(payload, filepath)

        latest_path = os.path.join(
            model_dir,
            f"{self.model_version}_latest.joblib"
        )
        joblib.dump(payload, latest_path)

        print(f"\n✓ Model saved to: {filepath}")
        print(f"✓ Latest model updated")

        return filepath

    @staticmethod
    def load_model(model_path):
        """
        Load a trained model from disk
        """
        data = joblib.load(model_path)
        return data["model"], data["feature_names"]
