from rest_framework import serializers
from Inventory.models import *


class RoomItemSerializer(serializers.ModelSerializer):
    flat = serializers.IntegerField(source='room.flat.flat_number', read_only=True)
    building = serializers.CharField(source='room.flat.building')

    class Meta:
        model = RoomItems
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    total_cost = serializers.SerializerMethodField(method_name='calculate_total_cost')
    building = serializers.CharField(source='flat.building.building_name', read_only=True)
    flat = serializers.IntegerField(source='flat.flat_number')
    items = RoomItemSerializer(many=True)

    class Meta:
        model = Room
        fields = '__all__'

    def calculate_total_cost(self, instance):
        all_items = RoomItems.objects.filter(room__room_name=instance.room_name,
                                             room__flat__flat_number=instance.flat.flat_number,
                                             room__flat__building_id=instance.flat.building.building_name)
        total_cost = 0
        for item in all_items:
            total_cost += item.cost
        return total_cost


class FlatSerializer(serializers.ModelSerializer):
    total_cost = serializers.SerializerMethodField(method_name='calculate_total_cost')
    rooms = RoomSerializer(many=True)

    class Meta:
        model = Flat
        fields = '__all__'

    def calculate_total_cost(self, instance):
        all_items = RoomItems.objects.filter(room__flat__flat_number=instance.flat_number,
                                             room__flat__building_id=instance.building.building_name)
        total_cost = 0
        for item in all_items:
            total_cost += item.cost
        return total_cost


class BuildingSerializer(serializers.ModelSerializer):
    total_cost = serializers.SerializerMethodField(method_name='calculate_total_cost')
    flats = FlatSerializer(many=True)

    class Meta:
        model = Building
        fields = '__all__'

    def calculate_total_cost(self, instance):
        all_items = RoomItems.objects.filter(room__flat__building_id=instance.building_name)
        total_cost = 0
        for item in all_items:
            total_cost += item.cost
        return total_cost
