from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import FriendRequest, Friend

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.ReadOnlyField(source='from_user.email')
    to_user = serializers.ReadOnlyField(source='to_user.email')
    status = serializers.CharField(read_only=True)

    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'status', 'created_at']

class FriendSerializer(serializers.ModelSerializer):
    friend = UserSerializer(read_only=True)

    class Meta:
        model = Friend
        fields = ['id', 'friend']

class UserSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']
