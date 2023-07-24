from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from flights_app.models import Profile


class ExtendedTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Customizes JWT default Serializer to add more information about user"""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token


class UserSerializer(ModelSerializer):

    password = serializers.CharField(
        max_length=128, validators=[validate_password], write_only=True)
    address = serializers.CharField(
        required=True, max_length=256, write_only=True
    )

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name', 'address']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'read_only': True},
        }
        validators = [UniqueTogetherValidator(User.objects.all(), ['email'])]

    def create(self, validated_data):
        with transaction.atomic():
            user = User.objects.create_user(
                username=validated_data['email'],
                email=validated_data['email'],
                password=validated_data['password'],
                first_name=validated_data.get('first_name', ''),
                last_name=validated_data.get('last_name', ''))
            Profile.objects.create(user=user, address=validated_data['address'])
        return user


class DetailedUserSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        fields = '__all__'
        model = Profile
