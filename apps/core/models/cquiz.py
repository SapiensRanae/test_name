from .quiz import Quiz
from django.db import models

class CQuiz(Quiz):

    trueAnswersP = models.IntegerField(default=0)
    triedTimes = models.IntegerField(default=0)

    parentQuiz = models.OneToOneField(Quiz, on_delete=models.CASCADE, parent_link=True, primary_key=True)

    startedAt = models.DateTimeField(auto_now_add=True)
    finishedAt = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"cquiz(id={self.id}, title={self.title}, trueAnswersP={self.trueAnswersP}, startedAt={self.startedAt}, finishedAt={self.finishedAt})"