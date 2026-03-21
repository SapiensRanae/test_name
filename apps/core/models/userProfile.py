'''
TODO:
=============================================================
WILL BE MOVED TO A SEPARATE APP LATER, BUT FOR NOW IT'S HERE
=============================================================

'''


from django.db import models
from .creator import Creator

class Gender(models.IntegerChoices):
    NOT_SPECIFIED = 0, 'Not specified'
    MALE = 1, 'Male'
    FEMALE = 2, 'Female'
    OTHER = 3, 'Other'

class UserProfile(models.Model):

    # main fields

    user = models.OneToOneField(Creator, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)


    bio = models.TextField(blank=True) # optional field for additional information
    gender = models.IntegerField(choices=Gender.choices, default=Gender.NOT_SPECIFIED)

    profilePictureUrl = models.URLField(blank=True) # optional field for profile picture

    #metadata fields
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    # getters, setters and overwrites

    def __str__(self) -> str:
        return self.user.name