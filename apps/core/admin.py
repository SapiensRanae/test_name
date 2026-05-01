from django.contrib import admin

from apps.core.models import QuizAttempt, QuizAttemptAnswer, QuizCollaborator


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
	list_display = ('id', 'quiz', 'takerName', 'user', 'score', 'maxScore', 'submittedAt')
	list_filter = ('quiz', 'submittedAt')
	search_fields = ('takerName',)


@admin.register(QuizAttemptAnswer)
class QuizAttemptAnswerAdmin(admin.ModelAdmin):
	list_display = ('id', 'attempt', 'question', 'selectedIndex', 'isCorrect', 'answeredAt')
	list_filter = ('isCorrect',)


@admin.register(QuizCollaborator)
class QuizCollaboratorAdmin(admin.ModelAdmin):
	list_display = ('id', 'quiz', 'creator', 'role', 'createdAt')
	list_filter = ('role',)
	search_fields = ('creator__email',)

# Register your models here.
