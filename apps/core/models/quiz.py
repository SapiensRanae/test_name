from django.db import models
from .question import Question


class Quiz(models.Model):

    # main fields

    title = models.CharField(max_length=255)
    description = models.TextField() # optional field for additional information


    maxSeconds = models.IntegerField(default=0) # optional field for time limit, 0 means no time limit

    # optional field for time limit per question, 0 means no time limit
    # can be overwritten by question's maxSecondsPerQuestion if it's set
    maxSecondsPerQuestion = models.IntegerField(default=0)



    #connections
    # owner = models.ForeignKey('Creator', on_delete=models.CASCADE)
    # questions = models.ManyToOneRel(Question)


    #metadata fields
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    # getters, setters and overwrites

    def __str__(self)-> str:
        return self.title