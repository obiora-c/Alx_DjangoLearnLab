

# notifications/serializers.py
from rest_framework import serializers
from .models import Notification
from accounts.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    actor = UserSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = ["id", "recipient", "actor", "verb", "target_object_id", "timestamp", "read"]
        read_only_fields = ["recipient", "actor", "verb", "target_object_id", "timestamp"]
