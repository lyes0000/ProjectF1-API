from rest_framework import serializers

class RacePredictionSerializer(serializers.Serializer):
    position = serializers.IntegerField()
    driver_id = serializers.IntegerField()
    driver_full_name = serializers.CharField()
    team = serializers.CharField(max_length=20)
    points = serializers.IntegerField()
    win_probability = serializers.FloatField()

    