from rest_framework import serializers
from .models import Post, Comment
from accounts.serializers import UserAccountSerializer

class PostSerializer(serializers.ModelSerializer):
    author = UserAccountSerializer(read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def validate_title(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        if len(value) > 200:
            raise serializers.ValidationError("Title cannot exceed 200 characters.")
        return value.strip()
    
    def validate_content(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value.strip()
    
    def create(self, validated_data):
        # Automatically set the author from the request user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class CommentSerializer(serializers.ModelSerializer):
    author = UserAccountSerializer(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def validate_content(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Content cannot be empty.")
        return value.strip()
    
    def validate_post(self, value):
        if not value:
            raise serializers.ValidationError("Post is required.")
        return value
    
    def create(self, validated_data):
        # Automatically set the author from the request user
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)