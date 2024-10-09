from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse
from tasks.models import Tasks


class AuthenticationTests(APITestCase):
    def test_user_registration(self):
        print("Test authentication")
        url = reverse('register')
        data = {
            "first_name": "new",
            "second_name": "user",
            "username": "newuser",
            "password_first": "newuserpassword",
            "password_second": "newuserpassword",
            "email": "newuser@test.com"
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())


class JWTAuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_and_obtain_jwt(self):
        print("Test login")
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

        self.refresh_token = response.data['refresh']

    def test_refresh_jwt_token(self):
        print("Test refresh token")
        self.test_login_and_obtain_jwt()

        url = reverse('token_refresh')
        data = {
            'refresh': self.refresh_token
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)


class TaskViewTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')
        self.task_user1 = Tasks.objects.create(owner=self.user1, title='Task User 1', description='Description 1')
        self.task_user2 = Tasks.objects.create(owner=self.user2, title='Task User 2', description='Description 2')

    def test_user_only_sees_own_tasks(self):
        print("Test get_list_tasks")
        url = reverse('get_list_tasks')

        self.client.login(username='user1', password='password1')

        response = self.client.get(url)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Task User 1')