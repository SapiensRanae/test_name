from uuid import uuid4

from django.db import models

from .question import Question
from .creator import Creator


class Quiz(models.Model):
    # main fields

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    # optional field for additional information

    maxSeconds = models.IntegerField(default=0)  # optional field for time limit, 0 means no time limit

    # optional field for time limit per question, 0 means no time limit
    # can be overwritten by question's maxSecondsPerQuestion if it's set
    maxSecondsPerQuestion = models.IntegerField(default=0)

    # connections
    creator = models.ManyToManyField(Creator, blank=False)
    # questions = models.ManyToManyField(Question, blank=True)
    # moved to Question with one to many relationship

    # metadata fields
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    publicToken = models.UUIDField(default=uuid4, unique=True, editable=False)
    publicTokenEnabled = models.BooleanField(default=True, verbose_name="Public access")

    # getters, setters and overwrites

    def __str__(self) -> str:
        return self.title
