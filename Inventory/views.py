from django.shortcuts import render
from rest_framework.response import Response
from Inventory.models import Building, Flat, Room, RoomItems
from rest_framework.views import APIView
from .serializer import BuildingSerializer, FlatSerializer, RoomSerializer, RoomItemSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework import status


class RoomItemsView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'Error': 'Unauthorized person', 'message': 'Login please'},
                            status=status.HTTP_401_UNAUTHORIZED)

        items = RoomItems.objects.all()
        serializer = RoomItemSerializer(items, many=True)

        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'Error': 'Unauthorized person', 'message': 'Login please'},
                            status=status.HTTP_401_UNAUTHORIZED)

        if not request.data:
            return Response({'Error': 'Bad Request', 'message': 'Please enter valid body'},
                            status=status.HTTP_400_BAD_REQUEST)

        item_name = request.data.get('item_name')
        room_id = request.data.get('room_id')
        cost = request.data.get('cost')
        if not item_name or not room_id or not cost:
            return Response({'Error': 'Bad Request', 'message': 'Please enter valid parameters'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            room = Room.objects.get(id=room_id)
            new_item = RoomItems(item_name=item_name, room=room, cost=cost)
            new_item.save()
            return Response({'status': 'Created', 'message': 'Item Created'}, status=status.HTTP_201_CREATED)
        except Room.DoesNotExist:
            return Response({'Error': 'Bad Request', 'message': 'Please enter valid room_id'},
                            status=status.HTTP_400_BAD_REQUEST)


class ItemView(APIView):
    def get(self, request, item_id):

        if not request.user.is_authenticated:
            return Response({'Error': 'Unauthorized person', 'message': 'Login please'},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            item = RoomItems.objects.get(id=item_id)
            serializer = RoomItemSerializer(item)
            return Response(serializer.data)
        except RoomItems.DoesNotExist:
            return Response({'Error': 'Not Found', 'message': 'Item Not Found'},
                            status=status.HTTP_404_NOT_FOUND)

    def put(self, request, item_id):
        if not request.user.is_authenticated:
            return Response({'Error': 'Unauthorized person', 'message': 'Login please'},
                            status=status.HTTP_401_UNAUTHORIZED)

        if not request.data:
            return Response({'Error': 'Bad Request', 'message': 'Please enter valid body'},
                            status=status.HTTP_400_BAD_REQUEST)

        item_name = request.data.get('item_name')
        room_id = request.data.get('room_id')
        cost = request.data.get('cost')
        try:
            item = RoomItems.objects.get(id=item_id)
            if item_name:
                item.item_name = item_name
            if cost:
                item.cost = cost
            if room_id:
                room = Room.objects.get(id=room_id)
                item.room = room
            item.save()
            return Response({'status': 'OK', 'message': 'Item Updated'},
                            status=status.HTTP_200_OK)
        except RoomItems.DoesNotExist:
            return Response({'Error': 'Not Found', 'message': 'Item Not Found'},
                            status=status.HTTP_404_NOT_FOUND)
        except Room.DoesNotExist:
            return Response({'Error': 'Not Found', 'message': 'Room Not Found'},
                            status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, item_id):
        if not request.user.is_authenticated:
            return Response({'Error': 'Unauthorized person', 'message': 'Login please'},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            item = RoomItems.objects.get(id=item_id)
            item.delete()
            return Response({'Error': 'OK', 'message': 'Item Deleted'},
                            status=status.HTTP_200_OK)
        except RoomItems.DoesNotExist:
            return Response({'Error': 'Not Found', 'message': 'Item Not Found'},
                            status=status.HTTP_404_NOT_FOUND)


class RoomsView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'Error': 'Unauthorized person', 'message': 'Login please'},
                            status=status.HTTP_401_UNAUTHORIZED)

        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)

        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'Error': 'Unauthorized person', 'message': 'Login please'},
                            status=status.HTTP_401_UNAUTHORIZED)

        if not request.data:
            return Response({'Error': 'Bad Request', 'message': 'Please enter valid body'},
                            status=status.HTTP_400_BAD_REQUEST)

        room_name = request.data.get('room_name')
        flat_id = request.data.get('flat_id')
        if not room_name or not flat_id:
            return Response({'Error': 'Bad Request', 'message': 'Please enter room_name or flat_id'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            flat = Flat.objects.get(id=flat_id)
            new_room = Room(room_name=room_name, flat=flat)
            new_room.save()
            return Response({'status': 'success', 'message': 'Room Created'}, status=status.HTTP_201_CREATED)
        except Flat.DoesNotExist:
            return Response({'Error': 'Not Found', 'message': 'Invalid Flat ID'},
                            status=status.HTTP_404_NOT_FOUND)


class RoomView(APIView):
    def get(self, request, room_id):

        if not request.user.is_authenticated:
            return Response({'Error': 'Unauthorized person', 'message': 'Login please'},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            item = Room.objects.get(id=room_id)
            serializer = RoomSerializer(item)
            return Response(serializer.data)
        except RoomItems.DoesNotExist:
            return Response({'Error': 'Not Found', 'message': 'Item Not Found'},
                            status=status.HTTP_404_NOT_FOUND)

    def put(self, request, room_id):
        if not request.user.is_authenticated:
            return Response({'Error': 'Unauthorized person', 'message': 'Login please'},
                            status=status.HTTP_401_UNAUTHORIZED)

        if not request.data:
            return Response({'Error': 'Bad Request', 'message': 'Please enter valid body'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            room = Room.objects.get(id=room_id)
            room_name = request.data.get('room_name')
            flat_id = request.data.get('flat_id')
            if room_name:
                room.room_name = room_name
            if flat_id:
                flat = Flat.objects.get(id=flat_id)
                room.flat = flat
            room.save()
            return Response({'status': 'OK', 'message': 'Room Updated'}, status=status.HTTP_200_OK)
        except Room.DoesNotExist:
            return Response({'Error': 'Not Found', 'message': 'Invalid Room ID'},
                            status=status.HTTP_404_NOT_FOUND)
        except Flat.DoesNotExist:
            return Response({'Error': 'Not Found', 'message': 'Invalid Flat ID'},
                            status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, room_id):
        if not request.user.is_authenticated:
            return Response({'Error': 'Unauthorized person', 'message': 'Login please'},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            room = Room.objects.get(id=room_id)
            room.delete()
            return Response({'status': 'OK', 'message': 'Room Deleted'}, status=status.HTTP_200_OK)
        except Room.DoesNotExist:
            return Response({'Error': 'Not Found', 'message': 'Invalid Room ID'},
                            status=status.HTTP_404_NOT_FOUND)


class FlatsView(APIView):

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'Error': 'Unauthorized person', 'message': 'Login please'},
                            status=status.HTTP_401_UNAUTHORIZED)

        flats = Flat.objects.all()
        serializer = FlatSerializer(flats, many=True)

        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'Error': 'Unauthorized person', 'message': 'Login please'},
                            status=status.HTTP_401_UNAUTHORIZED)

        if not request.data:
            return Response({'Error': 'Bad Request', 'message': 'Please enter valid body'},
                            status=status.HTTP_400_BAD_REQUEST)

        flat_number = request.data.get('flat_number')
        room_count = request.data.get('room_count')
        building_name = request.data.get('building_name')
        if not flat_number or not room_count:
            return Response({'Error': 'Bad Request', 'message': 'invalid flat or room_count'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            building = Building.objects.get(building_name=building_name)
            new_flat = Flat(flat_number=flat_number, room_count=room_count, building=building)
            new_flat.save()
            return Response({'status': 'Created', 'message': 'Flat is created.'},
                            status=status.HTTP_201_CREATED)
        except Building.DoesNotExist:
            return Response({'Error': 'Not Found', 'message': 'Invalid Building Name'},
                            status=status.HTTP_404_NOT_FOUND)


class FlatView(APIView):

    def get(self, request, flat_id):

        if not request.user.is_authenticated:
            return Response({'Error': 'Unauthorized person', 'message': 'Login please'},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            flat = Flat.objects.get(id=flat_id)
            serializer = FlatSerializer(flat)
            return Response(serializer.data)
        except RoomItems.DoesNotExist:
            return Response({'Error': 'Not Found', 'message': 'Item Not Found'},
                            status=status.HTTP_404_NOT_FOUND)

    def put(self, request, flat_id):
        if not request.user.is_authenticated:
            return Response({'Error': 'Unauthorized person', 'message': 'Login please'},
                            status=status.HTTP_401_UNAUTHORIZED)

        if not request.data:
            return Response({'Error': 'Bad Request', 'message': 'Please enter valid body'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            flat = Flat.objects.get(id=flat_id)
            flat_number = request.data.get('flat_number')
            room_count = request.data.get('room_count')
            building_name = request.data.get('building_name')
            if flat_number:
                flat.flat_number = flat_number
            if room_count:
                flat.room_count = room_count
            if building_name:
                building = Building.objects.get(building_name=building_name)
                flat.building = building
            flat.save()
            return Response({'status': 'OK', 'message': 'Flat Updated'}, status=status.HTTP_200_OK)
        except Flat.DoesNotExist:
            return Response({'Error': 'Not Found', 'message': 'Invalid Flat ID'},
                            status=status.HTTP_404_NOT_FOUND)
        except Building.DoesNotExist:
            return Response({'Error': 'Not Found', 'message': 'Invalid Building Name'},
                            status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, flat_id):
        if request.user.is_authenticated:
            return Response({'Error': 'Unauthorized person', 'message': 'Login please'},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            flat = Flat.objects.get(id=flat_id)
            flat.delete()
            return Response({'status': 'OK', 'message': 'Flat Deleted'}, status=status.HTTP_200_OK)
        except Flat.DoesNotExist:
            return Response({'Error': 'Not Found', 'message': 'Invalid Flat ID'},
                            status=status.HTTP_404_NOT_FOUND)


class BuildingsView(APIView):

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'Error': 'Unauthorized person', 'message': 'Login please'},
                            status=status.HTTP_401_UNAUTHORIZED)

        buildings = Building.objects.all()
        serializer = BuildingSerializer(buildings, many=True)

        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'Error': 'Unauthorized person', 'message': 'Login please'},
                            status=status.HTTP_401_UNAUTHORIZED)

        if not request.data:
            return Response({'Error': 'Bad Request', 'message': 'Please enter valid body'},
                            status=status.HTTP_400_BAD_REQUEST)

        name = request.data.get('building_name')
        flat_count = request.data.get('flat_count')
        if not name or not flat_count:
            return Response({'Error': 'Bad Request', 'message': 'invalid name or count'},
                            status=status.HTTP_400_BAD_REQUEST)
        building = Building.objects.filter(building_name=name)
        if building:
            return Response({'Error': 'Conflict', 'message': 'Building already exists'},
                            status=status.HTTP_409_CONFLICT)
        new_building = Building(building_name=name, flat_count=flat_count)
        new_building.save()
        return Response({'Status': 'Created', 'message': 'Building Created'}, status.HTTP_201_CREATED)


class BuildingView(APIView):

    def get(self, request, building_name):
        if not request.user.is_authenticated:
            return Response({'Error': 'Unauthorized person', 'message': 'Login please'},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            building = Building.objects.get(building_name=building_name)
            serializer = BuildingSerializer(building)
            return Response(serializer.data)
        except RoomItems.DoesNotExist:
            return Response({'Error': 'Not Found', 'message': 'Item Not Found'},
                            status=status.HTTP_404_NOT_FOUND)

    def put(self, request, building_name):
        if not request.user.is_authenticated:
            return Response({'Error': 'Unauthorized person', 'message': 'Login please'},
                            status=status.HTTP_401_UNAUTHORIZED)

        if not request.data:
            return Response({'Error': 'Bad Request', 'message': 'Please enter valid body'},
                            status=status.HTTP_400_BAD_REQUEST)
        name = request.data.get('building_name')
        flat_count = request.data.get('flat_count')

        try:
            building = Building.objects.get(building_name=building_name)
            if flat_count:
                building.flat_count = flat_count
            if name:
                building.building_name = name
            building.save()
        except Building.DoesNotExist:
            return Response({'Error': 'Not Found', 'message': 'Building not found'},
                            status=status.HTTP_404_NOT_FOUND)

        return Response({'Status': 'Created', 'message': 'Building Updated'}, status.HTTP_200_OK)

    def delete(self, request, building_name):
        if not request.user.is_authenticated:
            return Response({'Error': 'Unauthorized person', 'message': 'Login please'},
                            status=status.HTTP_401_UNAUTHORIZED)

        if not request.data:
            return Response({'Error': 'Bad Request', 'message': 'Please enter valid body'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            building = Building.objects.get(building_name=building_name)
            building.delete()
        except Building.DoesNotExist:
            return Response({'Error': 'Not Found', 'message': 'Building not found'},
                            status=status.HTTP_404_NOT_FOUND)

        return Response({'Status': 'Created', 'message': 'Building deleted'}, status.HTTP_200_OK)


class RegisterView(APIView):

    def post(self, request):
        if not request.data:
            return Response({'status': 'Bad Request', 'Error': 'Enter valid request body'},
                            status=status.HTTP_400_BAD_REQUEST)
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'status': 'Bad Request', 'Error': 'Enter username or password'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            if user:
                return Response({'status': 'Conflict', 'Error': 'Username already exists'},
                                status=status.HTTP_409_CONFLICT)
        except User.DoesNotExist:
            new_user = User.objects.create_user(username=username, password=password)
            new_user.save()
            return Response({'status': 'Created', 'message': 'User Created'}, status=status.HTTP_201_CREATED)


class AuthView(APIView):

    def post(self, request):
        if not request.data:
            return Response({'status': 'Bad Request', 'Error': 'Enter valid request body'},
                            status=status.HTTP_400_BAD_REQUEST)
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'status': 'Bad Request', 'Error': 'Enter username or password'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
            if user:
                auth = authenticate(request, username=username, password=password)
                if auth is not None:
                    login(request, auth)
                    return Response({'status': 'OK', 'message': 'login successful'},
                                    status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'status': 'Bad Request', 'message': 'Invalid username or password'},
                            status=status.HTTP_404_NOT_FOUND)


class IndexView(APIView):

    def get(self, request):
        return Response({'message': 'Welcome to inventory app. Please go to login or register page'})
