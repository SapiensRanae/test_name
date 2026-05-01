from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.core.models import Creator, Quiz, QuizCollaborator


class CollaborationAccessTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.owner_user = User.objects.create_user(username='owner', email='owner@example.com', password='pass1234')
        self.viewer_user = User.objects.create_user(username='viewer', email='viewer@example.com', password='pass1234')

        self.owner_creator = Creator.objects.create(email='owner@example.com')
        self.viewer_creator = Creator.objects.create(email='viewer@example.com')

        self.quiz = Quiz.objects.create(title='Q', description='D')
        self.quiz.creator.add(self.owner_creator)

        QuizCollaborator.objects.create(quiz=self.quiz, creator=self.viewer_creator, role='results_viewer')

    def test_results_viewer_can_open_results_page(self):
        self.client.force_login(self.viewer_user)
        url = reverse('quiz_results', kwargs={'pk': self.quiz.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_results_viewer_cannot_open_quiz_detail_edit_page(self):
        self.client.force_login(self.viewer_user)
        url = reverse('quiz_detail', kwargs={'pk': self.quiz.id})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)

