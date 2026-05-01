import json

from django.test import TestCase
from django.urls import reverse
from django.test.utils import override_settings
from django.core import mail

from django.contrib.auth import get_user_model

from apps.core.models import Quiz, Question, QuizAttempt


class PublicQuizFlowTests(TestCase):
    def setUp(self):
        self.quiz = Quiz.objects.create(title='Public Quiz', description='Desc')
        self.q1 = Question.objects.create(
            title='Q1',
            answerRight=1,
            answerOptions=json.dumps(['A', 'B', 'C']),
            explanation='exp1',
            InQuiz=self.quiz,
        )
        self.q2 = Question.objects.create(
            title='Q2',
            answerRight=0,
            answerOptions=json.dumps(['Yes', 'No']),
            explanation='exp2',
            InQuiz=self.quiz,
        )

    def test_public_take_page_loads(self):
        url = reverse('public_quiz_take', kwargs={'pk': self.quiz.id, 'token': self.quiz.publicToken})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.quiz.title)
        self.assertContains(resp, 'Your name')
        self.assertContains(resp, self.q1.title)

    def test_public_submit_shows_result(self):
        url = reverse('public_quiz_submit', kwargs={'pk': self.quiz.id, 'token': self.quiz.publicToken})
        payload = {
            'takerName': 'Alice',
            f'q_{self.q1.id}': '1',
            f'q_{self.q2.id}': '1',
        }
        resp = self.client.post(url, data=payload)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Results')
        self.assertContains(resp, 'Alice')
        self.assertContains(resp, '1/2')

        self.assertEqual(QuizAttempt.objects.filter(quiz=self.quiz).count(), 1)
        attempt = QuizAttempt.objects.get(quiz=self.quiz)
        self.assertEqual(attempt.takerName, 'Alice')
        self.assertEqual(attempt.score, 1)
        self.assertEqual(attempt.maxScore, 2)

    def test_logged_in_attempt_history(self):
        User = get_user_model()
        user = User.objects.create_user(username='u1', password='pass1234')
        self.client.force_login(user)

        url = reverse('public_quiz_submit', kwargs={'pk': self.quiz.id, 'token': self.quiz.publicToken})
        payload = {
            'takerName': 'Bob',
            f'q_{self.q1.id}': '1',
            f'q_{self.q2.id}': '0',
        }
        self.client.post(url, data=payload)

        history_url = reverse('my_attempts')
        resp = self.client.get(history_url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'My Attempts')
        self.assertContains(resp, self.quiz.title)

    def test_public_take_requires_token_enabled(self):
        self.quiz.publicTokenEnabled = False
        self.quiz.save(update_fields=['publicTokenEnabled'])
        url = reverse('public_quiz_take', kwargs={'pk': self.quiz.id, 'token': self.quiz.publicToken})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 404)

    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        QUIZ_RESULTS_EMAIL_ENABLED=True,
        DEFAULT_FROM_EMAIL='no-reply@test.local',
    )
    def test_public_submit_sends_email_when_enabled(self):
        from apps.core.models import Creator

        Creator.objects.create(email='creator1@example.com')
        self.quiz.creator.add(Creator.objects.get(email='creator1@example.com'))

        url = reverse('public_quiz_submit', kwargs={'pk': self.quiz.id, 'token': self.quiz.publicToken})
        payload = {
            'takerName': 'Alice',
            f'q_{self.q1.id}': '1',
            f'q_{self.q2.id}': '1',
        }
        self.client.post(url, data=payload)

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Quiz submission', mail.outbox[0].subject)
        self.assertIn('Alice', mail.outbox[0].body)
        self.assertIn('1/2', mail.outbox[0].body)
        self.assertIn('creator1@example.com', mail.outbox[0].to)



