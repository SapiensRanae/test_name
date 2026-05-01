from django.test import TestCase, Client
from django.urls import reverse
from apps.core.models import Quiz, Question, QuizAttempt, Creator, QuizCollaborator
from django.contrib.auth import get_user_model

User = get_user_model()


class IncompleteAttemptTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.creator = Creator.objects.create(email='test@example.com')
        self.quiz = Quiz.objects.create(title='Test Quiz', publicTokenEnabled=True)
        self.quiz.creator.add(self.creator)
        self.question = Question.objects.create(title='Q1', answerOptions='["A", "B"]', answerRight=0, InQuiz=self.quiz)

    def test_start_quiz_creates_attempt(self):
        url = reverse('public_quiz_start', kwargs={'pk': self.quiz.id, 'token': self.quiz.publicToken})
        response = self.client.post(url, {'takerName': 'John Doe'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('attempt_id', data)

        attempt = QuizAttempt.objects.get(id=data['attempt_id'])
        self.assertEqual(attempt.takerName, 'John Doe')
        self.assertIsNone(attempt.submittedAt)

    def test_incomplete_attempt_visible_to_creator(self):
        attempt = QuizAttempt.objects.create(quiz=self.quiz, takerName='John Doe', maxScore=1)
        self.client.login(username='testuser', password='password')
        url = reverse('quiz_results', kwargs={'pk': self.quiz.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')
        self.assertContains(response, 'In Progress')

    def test_incomplete_attempt_details(self):
        attempt = QuizAttempt.objects.create(quiz=self.quiz, takerName='John Doe', maxScore=1)
        from apps.core.models import QuizAttemptAnswer
        QuizAttemptAnswer.objects.create(attempt=attempt, question=self.question, selectedIndex=1, isCorrect=False)

        self.client.login(username='testuser', password='password')
        url = reverse('quiz_attempt_detail', kwargs={'quiz_pk': self.quiz.id, 'attempt_pk': attempt.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John Doe')
        self.assertContains(response, 'In Progress')
        self.assertContains(response, 'Q1')
        self.assertContains(response, 'Selected: B')
