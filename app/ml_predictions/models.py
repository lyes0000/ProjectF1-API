from django.db import models
from races.models import Race, RaceResult
from drivers.models import Driver
import json

class PredictionRun(models.Model):
    """
    Stores metadata about each Prediction Run
    """
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name='predictions')
    model_version = models.CharField(max_length=50) # for example "random_forest_v1"
    created_at = models.DateTimeField(auto_now_add=True)
    accuracy_score = models.FloatField(null=True, blank=True) # if we know results

    #model_config
    features_used = models.JSONField(default=list)
    model_params = models.JSONField(default=dict)

    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Prediction for {self.race} - {self.model_version}"
    
class DriverPrediction(models.Model):
    """
    Stores individual Driver Predictions for a race
    """
    prediction_run = models.ForeignKey(PredictionRun, on_delete=models.CASCADE, related_name='driver_predictions')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)

    # Predictions
    predicted_position = models.IntegerField()
    predicted_points = models.FloatField()
    win_probability = models.FloatField()
    podium_probability = models.FloatField()

    # Actual results (filled after race)
    actual_position = models.IntegerField(null=True, blank=True)
    actual_points = models.FloatField(null=True, blank=True)

    # Feature values used for this prediction
    feature_values = models.JSONField(default=dict)

    class Meta:
        ordering = ['predicted_position']
        unique_together = ['prediction_run', 'driver']

    def __str__(self):
        return f"{self.driver.code} - P{self.predicted_position} ({self.prediction_run.race.name})"
    
    @property
    def was_accurate(self):
        """Check if prediction was accurate (within 2 positions)"""
        if self.actual_position:
            return abs(self.predicted_position - self.actual_position) <= 2
        return None
    
class ModelPerformance(models.Model):
    """
    Tracks Model Performance over time
    """
    model_version = models.CharField(max_length=50)
    evaluated_at = models.DateTimeField(auto_now_add=True)

    # Perf metrics
    overall_accuracy = models.FloatField()
    within_2_accuracy = models.FloatField()
    podium_accuracy = models.FloatField()
    winner_accuracy = models.FloatField()

    # Data used
    training_races_count = models.IntegerField()
    total_races_count = models.IntegerField()

    # Detailed metrics
    metric_details = models.JSONField(default=dict)

    class Meta:
        ordering = ['evaluated_at']

    def __str__(self):
        return f"{self.model_version} - {self.overall_accuracy:.1f}% accuracy"