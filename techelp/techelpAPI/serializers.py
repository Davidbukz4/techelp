from rest_framework import serializers
from .models import Enduser, ITSupport, Ticket
import bleach
import imghdr

def validate_username(username):
  if len(username) < 3:
    raise serializers.ValidationError("Username must be at least 3 characters long.")
  return bleach.clean(username)

def validate_email(email):
  if not email:
    raise serializers.ValidationError("Email address is required.")
  return email

def validate_password(password):
  if len(password) < 8:
    raise serializers.ValidationError("Password must be at least 8 characters long.")
  return password

def validate_ticket_title(title):
  if not title:
    raise serializers.ValidationError("Ticket title is required.")
  return bleach.clean(title)

def validate_ticket_description(description):
  if not description:
    raise serializers.ValidationError("Ticket description is required.")
  return bleach.clean(description)

def validate_ticket_screenshot(screenshot):
    if not(screenshot):
        pass
    else:
        file_type = imghdr.what(screenshot)
        supported_file_types = ["jpeg", "jpg", "png", "gif"]
        if file_type not in supported_file_types:
            raise serializers.ValidationError("Screenshot must be a picture format")

class EnduserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[validate_username])
    email = serializers.EmailField(validators=[validate_email])
    password = serializers.CharField(validators=[validate_password])
    class Meta:
        model = Enduser
        fields = ['id', 'username', 'email', 'password']

class ITSupportSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[validate_username])
    email = serializers.EmailField(validators=[validate_email])
    password = serializers.CharField(validators=[validate_password])
    class Meta:
        model = ITSupport
        fields = ['id', 'username', 'email', 'password']

class TicketSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[validate_ticket_title])
    description = serializers.TextField(validators=[validate_ticket_description])
    screenshot = serializers.ImageField(validators=[validate_ticket_screenshot])
    owner = EnduserSerializer(read_only=True)
    class Meta:
        model = ITSupport
        fields = ['id', 'title', 'description', 'priority', 'status', 'category', 'owner', 'created_at', 'resolved_at', 'screenshot']
