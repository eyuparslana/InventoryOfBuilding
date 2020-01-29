from rest_framework import serializers
from Inventory.models import *


class RoomItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomItems
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):

    items = RoomItemSerializer(many=True)

    class Meta:
        model = Room
        fields = '__all__'


class FlatSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True)

    class Meta:
        model = Flat
        fields = '__all__'


class BuildingSerializer(serializers.ModelSerializer):
    total_cost = serializers.SerializerMethodField(method_name='calculate_total_cost')

    class Meta:
        model = Building
        fields = '__all__'

    def calculate_total_cost(self, instance):
        all_items = RoomItems.objects.filter(room__flat__building_id=instance.building_name)
        total_cost = 0
        for item in all_items:
            total_cost += item.cost
        return total_cost
