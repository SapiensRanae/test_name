from django import forms

from apps.core.models import Quiz


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = '__all__'
        exclude = ('createdAt', 'updatedAt', 'creator')