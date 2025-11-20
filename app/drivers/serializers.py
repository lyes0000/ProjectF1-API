from rest_framework import serializers
from drivers.models import Driver

class DriverSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = ['id', 'code', 'first_name', 'last_name', 'full_name', 'team', 'nationality', 'date_of_birth']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"