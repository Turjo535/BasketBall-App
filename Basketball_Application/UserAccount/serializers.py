from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model  = User
        fields = ("name", "email", "phone", "password", "password2")

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
        password = validated_data["password"]

        # Use your custom manager to create the user,
        # defaulting role to 'player'
        user = User.objects.create_user(
            name=name,
            email=email,
            phone=phone,
            role="player",
            password=password
        )
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    name= serializers.CharField(max_length=255)
    class Meta:
        model = User
        fields = ['name', 'password']
