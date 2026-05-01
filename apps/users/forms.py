from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser, UserProfile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'user'
        if commit:
            user.save()
        return user

class CustomUserUpdateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        # fields = ('username', 'email', 'avatar', 'password1', 'password2')
        fields = '__all__'
        exclude = [
            'created_at',
            'updated_at',

            'password',
            'password1',
            'password2',
            'groups',
            'first_name',
            'last_name',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = ''


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('name', 'surname', 'bio', 'gender', 'profilePictureUrl')
        exclude = ('user', 'createdAt', 'updatedAt')


