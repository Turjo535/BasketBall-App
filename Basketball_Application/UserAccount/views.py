from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserRegistrationSerializer, UserLoginSerializer, EmailValidationSerializer,OTPVerificationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

def get_tokens_for_user(user):
    if not user.is_active:
      raise AuthenticationFailed("User is not active")

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token= get_tokens_for_user(User)
            return Response({"message": f"User {user.name} registered successfully.", "tokens": token}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request, format=None):
        serializers = UserLoginSerializer(data=request.data)
        #print(serializers.data.get('email'))
        if serializers.is_valid(raise_exception=True):
            name = serializers.data.get('name')
            password = serializers.data.get('password')
            user = authenticate(name=name, password=password)


            if user is not None:
                token = get_tokens_for_user(user)
                return Response({
                    "Message": f"Welcome {user.name}",
                    "token": token
                }, status=status.HTTP_200_OK)
            else:
                return Response({"Error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EmailValidationView(APIView):
    def post(self, request):
        serializer = EmailValidationSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                return Response({"message": "Email is valid."}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "Email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

