from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('user', 'User'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')


class Gender(models.IntegerChoices):
    NOT_SPECIFIED = 0, 'Not specified'
    MALE = 1, 'Male'
    FEMALE = 2, 'Female'
    OTHER = 3, 'Other'


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255, blank=True)
    surname = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    gender = models.IntegerField(choices=[(0, 'Not specified'), (1, 'Male'), (2, 'Female'), (3, 'Other')], default=0)
    profilePictureUrl = models.URLField(blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} {self.surname}"


