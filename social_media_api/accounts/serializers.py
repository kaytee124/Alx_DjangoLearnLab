from rest_framework import serializers
from .models import useraccounts
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token

class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = useraccounts
        fields = ['id', 'username', 'email', 'bio', 'profile_picture']
        read_only_fields = ['id']

class UserAccountRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = useraccounts
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        # Create token for the newly registered user
        token = Token.objects.create(user=user)
        return {
            'user': UserAccountSerializer(user).data,
            'token': token.key
        }

class UserAccountLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_active:
            raise serializers.ValidationError('User is not active')
        
        # Get or create token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        return {
            'token': token.key,
            'user': UserAccountSerializer(user).data
        }