from django.contrib import admin
from django.urls import path, include
from .views import AdminDashboardView, OnlineUsersView

urlpatterns = [
    path('admindash/', AdminDashboardView.as_view(), name="admindashboard"),
    path('online_users/', OnlineUsersView.as_view(), name="online_users")
]