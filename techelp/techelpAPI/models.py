from django.db import models
#from django.contrib.auth.models import User

class Enduser(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)

    def __str__(self):
        return "End-user: {}".format(self.username)

class ITSupport(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=255)

    def __str__(self):
        return "IT Support: {}".format(self.username)

class Ticket(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.ChoiceField(
            choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")],)
    status = models.ChoiceField(
            choices=[("open", "Open"), ("in_progress", "In Progress"), ("resolved", "Resolved")],)
    category = models.ChoiceField(
            choices=[("software", "Software"), ("hardware", "Hardware"), ("network", "Network")],)
    owner = models.ForeignKey(Enduser, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(auto_now_add=True)
    screenshot = models.ImageField(upload_to="attachments/", blank=True, null=True)

    def __str__(self):
        return "Ticket({}) - User({})".format(self.id, self.owner)
