import joblib
import pandas as pd
import fastf1
from datetime import datetime

from ml_predictions.features.feature_builder import FeatureBuilder
from races.models import Race, RaceResult
from drivers.models import Driver



class RacePredictor:
    def __init__(self, model_path):
        data = joblib.load(model_path)
        self.model = data["model"]
        self.feature_names = data["feature_names"]
        self.feature_builder = FeatureBuilder()

    """def get_driver_for_race(self, race):
        
        #Returns participating drivers from DB or FastF1 if race is not in DB
        
        # Case 1: Race exists & has results
        if race and race.results.exists():
            return Driver.objects.filter(id__in=race.results.values_list("driver_id", flat=True)
            )
        
        # Case 2: Race is not in DB, future race to predict, we fetch from FastF1
    """

    def build_features(self, race):
        drivers = Driver.objects.all()

        driver_features = self.feature_builder.build_feature_for_race(
            race=race,
            drivers=drivers
        )

        X = driver_features[self.feature_names].fillna(0)
        return driver_features, X
    
    def predict(self, race):
        driver_features, X = self.build_features(race)

        win_probs = self.model.predict_proba(X)[:, 1]

        driver_features["win_probability"] = win_probs
        driver_features = driver_features.sort_values("win_probability", ascending=False)

        return driver_features[[
            "driver_id",
            "driver_code",
            "win_probability"
        ]]