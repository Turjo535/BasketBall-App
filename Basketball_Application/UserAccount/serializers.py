from rest_framework import serializers
from django.contrib.auth import get_user_model
from .utils import Util
import pyotp
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES)
    password  = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model  = User
        fields = ("name", "email", "phone", "role", "password", "password2")

    def validate(self, attrs):
        # Ensure password and confirmation match
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError(
                {"password2": "Password confirmation does not match."}
            )
        return attrs

    def create(self, validated_data):
        # Remove password2; only password remains
        print("Creating user with validated data:", validated_data)
        validated_data.pop("password2")
        name     = validated_data["name"]
        email    = validated_data["email"]
        phone    = validated_data["phone"]
        role     = validated_data["role"]
        password = validated_data["password"]

        # Use your custom manager to create the user,
        # defaulting role to 'player'
        user = User.objects.create_user(
            name=name,
            email=email,
            phone=phone,
            role=role,
            password=password
        )
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    name= serializers.CharField(max_length=255)
    class Meta:
        model = User
        fields = ['name', 'password']


class EmailValidationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    class Meta:
        fields = ['email']

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is not registered.")
        else:
            user= User.objects.get(email=value)
            secret = pyotp.random_base32()
            totp = pyotp.TOTP(secret, interval=300) # 5 minutes validity
            otp = totp.now()
            # Store the OTP secret and send the OTP to the user
            print(user)
            user.otp_secret = otp
            user.otp_send_time = timezone.now()
            user.save()   
            
            Util.send_email({
                'subject': 'Password Reset',
                'body': f'Your OTP is: {otp}',
                'to_email': user.email
            })
        return value

# CHANGED: Added comments and improved OTP secret handling (should be stored/retrieved, not regenerated)
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    class Meta:
        fields = ['email', 'otp']

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("This email is not registered.")

        user = User.objects.get(email=email)

        # Retrieve the OTP secret stored for the user (should be set when sending OTP)
        
        
        if (timezone.now() - user.otp_send_time) > timedelta(minutes=5):
            raise serializers.ValidationError("OTP has expired. Please request a new one.")
        elif user.otp_secret!=otp:
            raise serializers.ValidationError("OTP secret not found for this user.")

        return attrs
