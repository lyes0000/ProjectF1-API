from django.urls import path
from . import views

app_name = 'races'

urlpatterns = [
    path('races/', views.RaceListView.as_view(), name='race-list'),
    path('races/<int:pk>/', views.RaceDatailView.as_view(), name='race-detail'),
    path('races/fetch/', views.fetch_race_view, name='fetch-race'),
    path('results/', views.RaceResultsListView.as_view(), name='race-results'),
]