from django.db import models
from .Question import Question


class Quiz(models.Model):

    # main fields

    title = models.CharField(max_length=255)
    description = models.TextField() # optional field for additional information
    questions = models.ManyToOneRel(Question)
    owner = models.ForeignKey('User', on_delete=models.CASCADE)

    #metadata fields
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    # getters, setters and overwrites

    def __str__(self)-> str:
        return self.title