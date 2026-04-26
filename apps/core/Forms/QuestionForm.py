from django import forms

from apps.core.models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        exclude = ('createdAt', 'updatedAt', 'InQuiz')