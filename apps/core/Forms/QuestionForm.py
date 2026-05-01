from django import forms
import json

from apps.core.models import Question


class QuestionForm(forms.ModelForm):
    answerOptionsText = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label='Answer options (one per line, max 6)',
    )

    class Meta:
        model = Question
        fields = '__all__'
        exclude = ('createdAt', 'updatedAt', 'InQuiz')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['answerOptions'].required = False
        if self.instance and getattr(self.instance, 'answerOptions', None):
            try:
                options = json.loads(self.instance.answerOptions)
                if isinstance(options, list):
                    self.initial['answerOptionsText'] = "\n".join([str(x) for x in options[:6]])
            except Exception:
                self.initial['answerOptionsText'] = ''

    def clean(self):
        cleaned = super().clean()

        raw = (cleaned.get('answerOptionsText') or '').strip()
        options = [line.strip() for line in raw.splitlines() if line.strip()]
        options = options[:6]
        if len(options) < 2:
            self.add_error('answerOptionsText', 'Please provide at least 2 answer options (one per line).')

        answer_right = cleaned.get('answerRight')
        if answer_right is None:
            self.add_error('answerRight', 'Select the correct option index (0 to 5).')
        else:
            try:
                answer_right = int(answer_right)
            except Exception:
                self.add_error('answerRight', 'Select the correct option index (0 to 5).')
            else:
                if answer_right < 0 or answer_right > 5:
                    self.add_error('answerRight', 'Correct option index must be between 0 and 5.')
                elif options and answer_right >= len(options):
                    self.add_error('answerRight', 'Correct option index must exist in the provided options.')

        cleaned['answerOptions'] = json.dumps(options)
        return cleaned
