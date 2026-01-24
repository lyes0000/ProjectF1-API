import joblib
import pandas as pd
import fastf1
from datetime import datetime

from ml_predictions.features.feature_builder import FeatureBuilder
from races.models import Race, RaceResult
from races.services import driver_resolver
from races.services.single_race_fetch_service import RaceFetchService
from drivers.models import Driver



class RacePredictor:
    def __init__(self, model_path):
        data = joblib.load(model_path)
        self.model = data["model"]
        self.feature_names = data["feature_names"]
        self.feature_builder = FeatureBuilder()
        self.fetch_service = RaceFetchService()

    def build_features(self, year, race_name):
        # 1 Try to get race from DB
        try:
            race = Race.objects.get(year=year, name=race_name)
        except Race.DoesNotExist:
            # 2 Race not in DB -> fetch & store via RaceFetchService
            race, _ = self.fetch_service.fetch_race_data(year, race_name=race_name)

        # 3 Resolve active drivers
        drivers = driver_resolver.resolve_active_race_driver(year, race_name)

        driver_features = self.feature_builder.build_feature_for_race(
            race=race,
            drivers=drivers
        )

        # 4 Fill missing columns with 0 to avoid KeyError
        for col in self.feature_names:
            if col not in driver_features.columns:
                driver_features[col] = 0

        X = driver_features[self.feature_names].fillna(0)
        return driver_features, X
    
    def predict(self, year, race_name):
        driver_features, X = self.build_features(year, race_name)

        win_probs = self.model.predict_proba(X)[:, 1]

        driver_features["win_probability"] = win_probs
        driver_features = driver_features.sort_values("win_probability", ascending=False)

        return driver_features[[
            "driver_id",
            "driver_code",
            "win_probability"
        ]]