from django.core.management.base import BaseCommand
from ml_predictions.training.train_model import ModelTrainer


class Command(BaseCommand):
    help = "Train ML model for race predictions"

    def add_arguments(self, parser):
        parser.add_argument(
            '--year-start',
            type=int,
            default=2019,
            help='First year of training data'
        )
        parser.add_argument(
            '--year-end',
            type=int,
            default=2024,
            help='Last year of training data'
        )
        parser.add_argument(
            '--model-version',
            type=str,
            default='random_forest_v1',
            help='Model version identifier'
        )

    def handle(self, *args, **options):
        year_start = options['year_start']
        year_end = options['year_end']
        model_version = options['model_version']
        
        self.stdout.write(f"Training model: {model_version}")
        self.stdout.write(f"Data range: {year_start}-{year_end}")
        
        # Initialize trainer
        trainer = ModelTrainer(model_version=model_version)
        
        # Prepare data
        X, y, dataset = trainer.prepare_data(year_start, year_end)
        
        # Train model
        model, metrics = trainer.train(X, y, dataset)
        
        # Save model
        model_path = trainer.save_model()
        
        self.stdout.write(self.style.SUCCESS(f"\n✓ Training complete!"))
        self.stdout.write(f"Model saved to: {model_path}")
        self.stdout.write(f"Test AUC: {metrics['test_auc']:.3f}")
        self.stdout.write(f"Top-3 accuracy: {metrics['top_3_accuracy']:.1%}")
        self.stdout.write(f"Top-5 accuracy: {metrics['top_5_accuracy']:.1%}")