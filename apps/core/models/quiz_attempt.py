from django.conf import settings
from django.db import models


class QuizAttempt(models.Model):
	quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='attempts')

	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.SET_NULL,
		null=True,
		blank=True,
		related_name='quiz_attempts',
	)

	takerName = models.CharField(max_length=255)

	startedAt = models.DateTimeField(auto_now_add=True)
	submittedAt = models.DateTimeField(null=True, blank=True)

	score = models.IntegerField(default=0)
	maxScore = models.IntegerField(default=0)

	def __str__(self) -> str:
		return f"attempt(id={self.id}, quiz={self.quiz_id}, score={self.score}/{self.maxScore})"


