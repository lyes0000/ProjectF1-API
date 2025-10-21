from django.shortcuts import render
from rest_framework import generics
from races.models import RaceResult
from .serializers import RaceResultSerializer

class RaceResultsListView(generics.ListAPIView):
    queryset = RaceResult.objects.select_related('driver', 'race')
    serializer_class = RaceResultSerializer