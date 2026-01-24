from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Q
from .models import Race, RaceResult
from .serializers import (
    RaceSerializer,
    RaceResultSerializer,
    FetchRaceRequestSerializer
)
from .services import RaceFetchService

# List all races
class RaceListView(generics.ListAPIView):
    """
    GET /api/races/
    Optional query params: ?year=2024
    """
    serializer_class = RaceSerializer

    def get_queryset(self):
        queryset = Race.objects.all().order_by('-year', '-round')

        # Filter by year if provided
        year = self.request.query_params.get('year')
        if year:
            queryset = queryset.filter(year=year)

        return queryset
    
# Get specific races with results
class RaceDatailView(generics.RetrieveAPIView):
    """GET /api/races/<id>/"""
    queryset = Race.objects.all()
    serializer_class = RaceSerializer

# Get race results with filtering
class RaceResultsListView(generics.ListAPIView):
    """
    GET /api/results/
    Query params: ?race=<id>, ?year=<year>, ?driver=<code>
    """
    serializer_class = RaceResultSerializer

    def get_queryset(self):
        queryset = RaceResult.objects.select_related('race', 'driver').all()

        # Filter by race
        race_id = self.request.query_params.get('race')
        if race_id:
            queryset = queryset.filter(race_id=race_id)

        # Filter by year
        year = self.request.query_params.get('year')
        if year:
            queryset = queryset.filter(race__year=year)

        # Filter by driver
        driver_code = self.request.query_params.get('driver')
        if driver_code:
            queryset = queryset.filter(driver__code=driver_code)

        return queryset.order_by('-race__year', '-race__round', 'position')
    
# Fetch new race data (POST endpoint)
@api_view(['POST'])
def fetch_race_view(request):
    """
    POST /api/races/fetch/
    Body examples:
    {"year": 2024, "round": "1"}
    {"year": 2024, "race_name": "Brazil"}
    """
    serializer = FetchRaceRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    year = serializer.validated_data['year']
    round = serializer.validated_data.get('round')
    race_name = serializer.validated_data.get('race_name')

    # Check if it exists already
    if Race.objects.filter(year=year, round=round).exists():
        return Response(
            {'message': 'Race already exists', 'status': 'exists'},
            status=status.HTTP_200_OK
        )
    
    try:
        service = RaceFetchService()
        race, created = service.fetch_race_data(
            year=year, 
            round=round,
            race_name=race_name
            )

        race_serializer = RaceSerializer(race)
        return Response(
            {
                'message': f'Race {"created" if created else "updated"} succesfully',
                'race': race_serializer.data
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
    except ValueError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'error': f'server error: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
