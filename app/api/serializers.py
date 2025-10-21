from rest_framework import serializers
from drivers.models import Driver
from races.models import Race, RaceResult

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
