# registration/forms.py
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'avatar', 'password1', 'password2', 'role')

class CustomUserUpdateForm(UserCreationForm):
    class Meta:
        model = CustomUser
        # fields = ('username', 'email', 'avatar', 'password1', 'password2')
        fields = '__all__'
        exclude = [
            'created_at',
            'updated_at',
            'avatar',
            'password',
            'password1',
            'password2',
            'groups',
            'first_name',
            'last_name',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Очищаємо help_text для кожного поля
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = ''
