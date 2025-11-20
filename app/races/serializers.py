from rest_framework import serializers
from drivers.serializers import DriverSerializer
from .models import Race, RaceResult

class RaceResultSerializer(serializers.ModelSerializer):
    driver = DriverSerializer()

    class Meta:
        model = RaceResult
        fields = ['id', 'driver', 'race', 'position', 'points', 'fastest_lap_time']

class RaceSerializer(serializers.ModelSerializer):
    results = RaceResultSerializer(many=True, read_only=True)

    class Meta:
        model = Race
        fields = ['id', 'name', 'circuit', 'year', 'round', 'date', 'results']
    
class FetchRaceRequestSerializer(serializers.Serializer):
    """
    Validates requests to fetch new race data
    Can use either round number OR race name
    """
    year = serializers.IntegerField(min_value=1950, max_value=2025)
    round = serializers.IntegerField(min_value=1, max_value=24, required=False)
    race_name = serializers.CharField(max_length=200, required=False)
    
    def validate(self, data):
        """Ensure at least one identifier is provided (round or race_name)"""
        if not data.get('round') and not data.get('race_name'):
            raise serializers.ValidationError(
                "Either 'round' or 'race_name' must be provided"
            )
        return data