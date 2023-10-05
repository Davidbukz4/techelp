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
    priority_choices = (("low", "Low"), ("medium", "Medium"), ("high", "High"))
    status_choices = (("open", "Open"), ("in_progress", "In Progress"), ("resolved", "Resolved"))
    category_choices = (("software", "Software"), ("hardware", "Hardware"), ("network", "Network"))
    priority = models.CharField(max_length=12, choices=priority_choices, default="low")
    status = models.CharField(max_length=12, choices=status_choices, default="open")
    category = models.CharField(max_length=12, choices=category_choices, default="software")
    owner = models.ForeignKey(Enduser, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    screenshot = models.ImageField(upload_to="attachments/", blank=True, null=True)

    def __str__(self):
        return "Ticket({}) - User({})".format(self.id, self.owner)
