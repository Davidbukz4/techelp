from rest_framework import serializers
from .models import Enduser, ITSupport, Ticket
import bleach

class EnduserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enduser
        fields = ['id', 'username', 'email', 'password']

class ITSupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ITSupport
        fields = ['id', 'username', 'email', 'password']

class TicketSerializer(serializers.ModelSerializer):
    owner = EnduserSerializer(read_only=True)
    def validate_title(self, value):
        return bleach.clean(value)
    def validate_description(self, value):
        return bleach.clean(value)
    def validate_screenshot(self, value):
        pass
    class Meta:
        model = ITSupport
        fields = ['id', 'title', 'description', 'priority', 'status', 'category', 'owner', 'created_at', 'resolved_at', 'screenshot']


