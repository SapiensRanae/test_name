from django import forms

from apps.core.models import CQuiz


class CQuizForm(forms.ModelForm):
    class Meta:
        model = CQuiz
        fields = '__all__'
        exclude = ('createdAt', 'updatedAt','parentQuiz')