from django import forms

from apps.core.models import Creator


class CreatorForm(forms.ModelForm):
    class Meta:
        model = Creator
        fields = '__all__'
        exclude = ('createdAt', 'updatedAt')