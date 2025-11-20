from django.urls import path
from . import views

app_name = 'drivers'

urlpatterns = [
    path('driver/', views.DriverListView.as_view(), name='driver-list'),
    path('drivers/<int:pk>/', views.DriverDetailView.as_view(), name='driver-details'),
]