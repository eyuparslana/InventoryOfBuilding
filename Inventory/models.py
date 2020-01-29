from django.db import models


class Building(models.Model):
    building_name = models.CharField(max_length=5, primary_key=True)
    flat_count = models.IntegerField()

    def __str__(self):
        return self.building_name


class Flat(models.Model):
    flat_number = models.IntegerField()
    room_count = models.IntegerField()
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='flats')

    def __str__(self):
        return "Flat: {}, Building: {}".format(self.flat_number, self.building)


class Room(models.Model):
    room_name = models.CharField(max_length=50)
    flat = models.ForeignKey(Flat, on_delete=models.CASCADE, related_name='rooms')

    def __str__(self):
        return "Room: {}, {}".format(self.room_name, self.flat)


class RoomItems(models.Model):
    item_name = models.CharField(max_length=50)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='items')
    cost = models.IntegerField()

    def __str__(self):
        return "Item: {}, {}".format(self.item_name, self.room)
