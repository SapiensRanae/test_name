from django.db import models


class QuizCollaborator(models.Model):
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('editor', 'Editor'),
        ('results_viewer', 'Results viewer'),
    ]

    quiz = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='collaborators')
    creator = models.ForeignKey('Creator', on_delete=models.CASCADE, related_name='quiz_roles')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='editor')

    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('quiz', 'creator')

    def __str__(self) -> str:
        return f"collaborator(quiz={self.quiz_id}, creator={self.creator_id}, role={self.role})"

