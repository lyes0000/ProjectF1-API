from rest_framework import serializers
from drivers.models import Driver
from races.models import Race, RaceResult
import math

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['first_name', 'last_name', 'code']

class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = ['name']
    
class RaceResultSerializer(serializers.ModelSerializer):
    driver = DriverSerializer()
    race = RaceSerializer()
    class Meta:
        model = RaceResult
        fields = ['driver', 'race','position', 'points', 'fastest_lap_time']

    def to_representation(self, instance):
        """Ensure no NaN or Infinity values break JSON."""
        data = super().to_representation(instance)
        for key, value in data.items():
            if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                data[key] = None
        return data