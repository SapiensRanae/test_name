from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class RegisterFlowTests(TestCase):
    def test_register_auto_logs_in_and_sets_user_role(self):
        url = reverse('register')
        payload = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'StrongPass12345',
            'password2': 'StrongPass12345',
            'role': 'admin',
        }
        resp = self.client.post(url, data=payload)
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(resp.headers.get('Location'), reverse('welcome'))

        User = get_user_model()
        u = User.objects.get(username='newuser')
        self.assertEqual(u.role, 'user')

        resp2 = self.client.get(reverse('welcome'))
        self.assertTrue(resp2.wsgi_request.user.is_authenticated)

