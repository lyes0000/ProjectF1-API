from django.shortcuts import render
from rest_framework import generics
from races.models import RaceResult
from .serializers import RaceResultSerializer

class RaceResultsListView(generics.ListAPIView):
    serializer_class = RaceResultSerializer

    def get_queryset(self):
        queryset = RaceResult.objects.select_related('driver', 'race')
        year = self.request.query_params.get('year')
        round_number = self.request.query_params.get('round')

        if year:
            queryset = queryset.filter(race__year=year)
        if round_number:
            queryset = queryset.filter(race__round=round_number)

        """Allows to display results by position number"""
        return queryset.order_by('position')