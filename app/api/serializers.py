from rest_framework import serializers
from drivers.models import Driver
from races.models import Race, RaceResult
import math

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = '__all__'

class RaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Race
        fields = '__all__'
    
class RaceResultSerializer(serializers.ModelSerializer):
    driver = DriverSerializer()
    class Meta:
        model = RaceResult
        fields = '__all__'

    def to_representation(self, instance):
        """Ensure no NaN or Infinity values break JSON."""
        data = super().to_representation(instance)
        for key, value in data.items():
            if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                data[key] = None
        return data