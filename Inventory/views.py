from django.shortcuts import render
from rest_framework.response import Response
from Inventory.models import *
from rest_framework.views import APIView
from .serializer import *
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
        pass


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
