from django.core.management.base import BaseCommand, CommandError
from races.models import Race
from ml_predictions.prediction.predict_race import RacePredictor

class Command(BaseCommand):
    help = "Predict race winner for a specific race"

    def add_arguments(self, parser):
        # Add optional arguments for year and race name
        parser.add_argument(
            "--year",
            type=int,
            required=True,
            help="Year of the race (e.g., 2025)"
        )
        parser.add_argument(
            "--name",
            type=str,
            required=True,
            help="Race name (e.g., 'Japanese Grand Prix')"
        )

    def handle(self, *args, **options):
        year = options["year"]
        name = options["name"]

        model_path = "ml_predictions/ml_models/random_forest_v1_latest.joblib"
        predictor = RacePredictor(model_path)
        
        try:
            predictions = predictor.predict(
                year=year,
                race_name=name
            )
        except Exception as e:
            raise Exception(f"prediction failed: {str(e)}")

        # Print results
        self.stdout.write(f"Predictions for {name} {year}:")
        self.stdout.write(predictions.to_string(index=False))