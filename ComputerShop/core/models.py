from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, EmailField, DateTimeField, BooleanField, ForeignKey, TextField
from django.utils import timezone



class Notification(models.Model):
    message = TextField()
    message_date = DateTimeField(default=timezone.now)
