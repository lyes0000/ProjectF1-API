from django.db import models
from drivers.models import Driver

class Race(models.Model):
    name = models.CharField(max_length=100)
    circuit = models.CharField(max_length=100)
    year = models.IntegerField()
    round = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return f"{self.name} {self.year}"
    
class RaceResult(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="results")
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    position = models.IntegerField()
    points = models.FloatField()
    fastest_lap_time = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.driver} - {self.race} - {self.position}"
    