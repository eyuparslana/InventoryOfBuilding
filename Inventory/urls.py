from django.contrib import admin
from django.urls import path, include
from Inventory import views

urlpatterns = [
    path('register', views.RegisterView.as_view()),
    path('buildings', views.BuildingsView.as_view()),
    path('auth', views.AuthView.as_view()),
]
