from django.contrib import admin
from django.urls import path, include
from Inventory import views

urlpatterns = [
    path('register', views.RegisterView.as_view()),
    path('buildings', views.BuildingsView.as_view()),
    path('auth', views.AuthView.as_view()),
    path('flats', views.FlatsView.as_view()),
    path('rooms', views.RoomsView.as_view()),
    path('items', views.RoomItemsView.as_view()),
    path('items/<int:item_id>', views.ItemView.as_view()),
    path('rooms/<int:room_id>', views.RoomView.as_view()),
    path('flats/<int:flat_id>', views.FlatView.as_view()),
    path('buildings/<str:building_name>', views.BuildingView.as_view())
]
