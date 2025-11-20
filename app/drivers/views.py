from rest_framework import generics
from django.db.models import Q, Count
from .models import Driver
from .serializers import DriverSerializer

class DriverListView(generics.ListAPIView):
    """
    GET /api/drivers/
    Optional query params: ?nationality=ITA, ?search=verstappen
    """
    serializer_class = DriverSerializer

    def get_queryset(self):
        queryset = Driver.objects.all().order_by('last_name', 'first_name')

        # Filter by nationality
        nationality = self.request.query_params.get('nationality')
        if nationality:
            queryset = queryset.filter(nationality__icontains=nationality)

        # Search by name or code
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(code__icontains=search)
            )

        return queryset
    
class DriverDetailView(generics.RetrieveAPIView):
    """
    GET /api/driver/<id>/
    Returns driver details with all their race results
    """
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer