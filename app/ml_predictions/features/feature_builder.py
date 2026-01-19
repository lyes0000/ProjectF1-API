"""
Builds feature matric for ML training/prediction
"""

import pandas as pd
from .feature_definitions import FeatureDefinitions, FEATURE_LIST

class FeatureBuilder:
    """
    Constructs Feature matrix from race data
    """

    def __init__(self):
        self.feature_defs = FeatureDefinitions()

    def build_feature_for_race(self, race, drivers):
        """
        Build Feature matric for all drivers in a race

        Args:
            race: Race object
            drivers: List of Driver objects

        Returns:
            DataFrame with features for each driver
        """
        feature_list = []

        for driver in drivers:
            driver_feature = {
                'race_id': race.id,
                'driver_id': driver.id,
                'driver_code': driver.code,
            }

            # Calculate each feature
            for feature_name in FEATURE_LIST:
                feature_func = getattr(self.feature_defs, feature_name)
                driver_feature[feature_name] = feature_func(driver.id, race)

            feature_list.append(driver_feature)

        return pd.DataFrame(feature_list)
    
    def build_training_dataset(self, races):
        """
        Build complete training dataset from multiple races

        Args:
            races: QuerySet of Race objects

        Returns:
            DataFrame with features and target (actual position)
        """
        from races.models import RaceResult

        all_features = []
        
        for race in races:
            # Get all results for this races
            results = RaceResult.objects.filter(race=race).select_related('driver')
            drivers = [result.driver for result in results]

            # Build features
            race_features = self.build_feature_for_race(race, drivers)

            # Add target variable (actual position)
            for idx, result in enumerate(results):
                race_features.loc[
                    race_features['driver_id'] == result.driver_id,
                    'position'
                ] = result.position
                race_features.loc[
                    race_features['driver_id'] == result.driver_id,
                    'points'
                ] = result.points

            all_features.append(race_features)

        return pd.concat(all_features, ignore_index=True)
    
    def get_feature_names(self):
        """Return list of feature column names"""
        return FEATURE_LIST