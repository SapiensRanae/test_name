'''
TODO:
=============================================================
WILL BE MOVED TO A SEPARATE APP LATER, BUT FOR NOW IT'S HERE
=============================================================

'''


from django.db import models
import uuid
from .Quiz import Quiz
from .UserProfile import UserProfile



class User(models.Model):
    # main fields

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    visibleName = models.CharField(max_length=255)
    email = models.EmailField(unique=True, null=False, blank=False)
    passwordHash = models.CharField(max_length=255)

    profile = models.OneToOneField('UserProfile', on_delete=models.CASCADE, null=True, blank=True)

    ownedQuizzes = models.ManyToManyField(Quiz, blank=True)  # quizzes that the user has saved or created

    #metadata fields
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    # getters, setters and overwrites

    def __str__(self)-> str:
        return self.name