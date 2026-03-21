from .quiz import Quiz
from django.db import models

class CQuiz(Quiz):

    trueAnswersP = models.IntegerField(default=0)
    triedTimes = models.IntegerField(default=0)

    startedAt = models.DateTimeField(auto_now_add=True)
    finishedAt = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"cquiz(id={self.id}, title={self.title}, trueAnswersP={self.trueAnswersP}, startedAt={self.startedAt}, finishedAt={self.finishedAt})"