from django.db import models


class QuizAttemptAnswer(models.Model):
	attempt = models.ForeignKey('QuizAttempt', on_delete=models.CASCADE, related_name='answers')
	question = models.ForeignKey('Question', on_delete=models.CASCADE, related_name='attempt_answers')

	selectedIndex = models.IntegerField(null=True, blank=True)
	isCorrect = models.BooleanField(default=False)

	answeredAt = models.DateTimeField(auto_now_add=True)

	def __str__(self) -> str:
		return f"attempt_answer(id={self.id}, attempt={self.attempt_id}, question={self.question_id})"


