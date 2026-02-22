from rest_framework import serializers
from .models import Notification
from accounts.serializers import UserAccountSerializer

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserAccountSerializer(read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'target', 'read', 'timestamp']
        read_only_fields = ['id', 'recipient', 'actor', 'verb', 'target', 'timestamp']
