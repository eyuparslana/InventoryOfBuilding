from django.shortcuts import render
from rest_framework.response import Response
from Inventory.models import Building
from rest_framework.views import APIView
from .serializer import BuildingSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework import status


class BuildingsView(APIView):

    def get(self, request):
        if request.user.is_authenticated:
            buildings = Building.objects.all()
            serializer = BuildingSerializer(buildings, many=True)

            return Response(serializer.data)
        else:
            return Response({'Error': 'Unauthorized person', 'message': 'Login please'},
                            status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        if request.user.is_authenticated:
            if request.data:
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
        else:
            return Response({'Error': 'Unauthorized person', 'message': 'Login please'},
                            status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        if request.user.is_authenticated:
            if request.data:
                name = request.data.get('building_name')
                flat_count = request.data.get('flat_count')
                if not name or not flat_count:
                    return Response({'Error': 'Bad Request', 'message': 'invalid name or count'},
                                    status=status.HTTP_400_BAD_REQUEST)
                try:
                    building = Building.objects.get(building_name=name)
                    building.flat_count = flat_count
                    building.save()
                except Building.DoesNotExist:
                    return Response({'Error': 'Not Found', 'message': 'Building not found'},
                                    status=status.HTTP_404_NOT_FOUND)

                return Response({'Status': 'Created', 'message': 'Building Updated'}, status.HTTP_200_OK)
        else:
            return Response({'Error': 'Unauthorized person', 'message': 'Login please'},
                            status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        if request.user.is_authenticated:
            if request.data:
                name = request.data.get('building_name')
                if not name:
                    return Response({'Error': 'Bad Request', 'message': 'invalid name or count'},
                                    status=status.HTTP_400_BAD_REQUEST)
                try:
                    building = Building.objects.get(building_name=name)
                    building.delete()
                except Building.DoesNotExist:
                    return Response({'Error': 'Not Found', 'message': 'Building not found'},
                                    status=status.HTTP_404_NOT_FOUND)

                return Response({'Status': 'Created', 'message': 'Building deleted'}, status.HTTP_200_OK)
        else:
            return Response({'Error': 'Unauthorized person', 'message': 'Login please'},
                            status=status.HTTP_401_UNAUTHORIZED)


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
