from django.urls import path
from . import views

app_name = 'drivers'

urlpatterns = [
    path('drivers/', views.DriverListView.as_view(), name='driver-list'),
    path('driver/<int:pk>/', views.DriverDetailView.as_view(), name='driver-details'),
]