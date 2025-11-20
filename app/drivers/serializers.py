from rest_framework import serializers
from drivers.models import Driver
import math

class DriverSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = ['id', 'code', 'first_name', 'last_name', 'full_name', 'team', 'nationality', 'date_of_birth']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    def to_representation(self, instance):
        """Ensure no NaN or Infinity values break JSON."""
        data = super().to_representation(instance)
        for key, value in data.items():
            if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
                data[key] = None
        return data