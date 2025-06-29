from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import UserRegistrationSerializer, UserLoginSerializer, EmailValidationSerializer,VerifyOTPSerializer,UserChangePasswordSerializer, ForgetPasswordResetSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime, timedelta


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
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        return Response({"message": "User logged out successfully."}, status=status.HTTP_200_OK)


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

class VerifyOTPView(APIView):
    
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user= User.objects.filter(email=email).first()

            user.otp_secret = None
            user.otp_send_time = None
            user.is_active = True
            user.save()
            return Response({"message": "OTP verified successfully. Account is activated."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        
        serializer = UserChangePasswordSerializer(data=request.data, context={'user':request.user})
        #print(serializer.data)
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'Password Changed Successfully'}, status=status.HTTP_200_OK)

class ForgetPasswordResetView(APIView):
    
    def post(self, request, format=None):
        serializer = ForgetPasswordResetSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
        
            return Response({"message": "Password Change Successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
