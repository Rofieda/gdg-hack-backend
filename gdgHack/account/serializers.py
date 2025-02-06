from rest_framework import serializers

from .models import User 

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from account.models import User

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import User
from rest_framework_simplejwt.exceptions import TokenError

from django.contrib.auth import authenticate

# ****************************************** auth ********************************************************

# Custom serializer to include user role in the JWT payload
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role  # Add custom claims
        return token


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials")
        
        attrs['user'] = user  # Add user to validated data
        return attrs

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        # Initialize an error dictionary
        errors = {}

        # Check if email is missing
        if not attrs.get('email'):
            errors['email'] = ['This field is required.']

        # Check if password is missing
        if not attrs.get('password'):
            errors['password'] = ['This field is required.']

        # Raise ValidationError if there are errors
        if errors:
            raise serializers.ValidationError(errors)

        return attrs  # Return validated attributes

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


   


# Serializer for logging out the user

class LogoutUserSerializer(serializers.Serializer):
    refresh = serializers.CharField()  # Expecting refresh token in the request body

    default_error_messages = {
        'bad_token': 'Token is expired or invalid.'
    }

    def validate(self, attrs):
        refresh = attrs.get('refresh')
        if not refresh:
            raise ValidationError({"refresh": "This field is required."})
        self.token = refresh
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()  # Blacklist the token (requires blacklisting enabled in SimpleJWT)
        except TokenError:
            raise ValidationError(self.default_error_messages['bad_token'])





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True},  #  password is write-only
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'patient')  
        )
        return user

