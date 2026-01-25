from django.urls import path
from .views import RacePredictionAPIView

urlpatterns = [
    path('predict/', RacePredictionAPIView.as_view(), name='race-prediction'),
]