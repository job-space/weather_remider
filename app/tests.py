from rest_framework import status
from rest_framework.test import APITestCase

from app.models import City, User


class CityTests(APITestCase):

    def setUp(self):
        user1 = User.objects.create(username='user1', password='mpzxqrbvsnpgkiwc', email='test123@gmail.com')
        City.objects.create(name='Malyn', notification_interval=4, user=user1)

    def test_user_reg(self):
        url = '/api/v1/auth/users/'
        data = {'username': 'user2',
                'password': 'mpzxqrbvsnpgkiwcss',
                'email': 'test12213@gmail.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_user_login(self):
        url = '/api/v1/auth/users/'
        data = {'username': 'user2',
                'password': 'mpzxqrbvsnpgkiwcss',
                'email': 'test12213@gmail.com'}
        self.client.post(url, data, format='json')
        response = self.client.login(username='user2', password='mpzxqrbvsnpgkiwcss')
        self.assertEqual(response, True)

    def test_city_get(self):
        url = '/api/v1/auth/users/'
        data = {'username': 'user2',
                'password': 'mpzxqrbvsnpgkiwcss',
                'email': 'test12213@gmail.com'}
        self.client.post(url, data, format='json')
        self.client.login(username='user2', password='mpzxqrbvsnpgkiwcss')

        response = self.client.get('http://127.0.0.1:8000/api/v1/city/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("OrderedDict([('name', 'Malyn'), ('notification_interval', 4), ('user', 1)])", f"{response.data['results'][0]}")

    def test_city_post(self):
        url = '/api/v1/auth/users/'
        data = {'username': 'user2',
                'password': 'mpzxqrbvsnpgkiwcss',
                'email': 'test12213@gmail.com'}
        self.client.post(url, data, format='json')
        self.client.login(username='user2', password='mpzxqrbvsnpgkiwcss')

        user2 = User.objects.get(username='user2')

        url = '/api/v1/city/'
        data = {'name': 'Malyn',
                'notification_interval': 6,
                'user': user2.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'name': 'Malyn', 'notification_interval': 6, 'user': 2})

    def test_city_put(self):
        url = '/api/v1/auth/users/'
        data = {'username': 'user2',
                'password': 'mpzxqrbvsnpgkiwcss',
                'email': 'test12213@gmail.com'}
        self.client.post(url, data, format='json')
        self.client.login(username='user2', password='mpzxqrbvsnpgkiwcss')

        user2 = User.objects.get(username='user2')

        url = '/api/v1/city/'
        data = {'name': 'Malyn',
                'notification_interval': 6,
                'user': user2.id}
        self.client.post(url, data, format='json')

        url = '/api/v1/city/2/'
        data = {'name': 'Tokyo',
                'notification_interval': 8,
                'user': user2.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'name': 'Tokyo', 'notification_interval': 8, 'user': 2})

    def test_city_delete(self):
        url = '/api/v1/auth/users/'
        data = {'username': 'user2',
                'password': 'mpzxqrbvsnpgkiwcss',
                'email': 'test12213@gmail.com'}
        self.client.post(url, data, format='json')
        self.client.login(username='user2', password='mpzxqrbvsnpgkiwcss')

        user2 = User.objects.get(username='user2')

        url = '/api/v1/city/'
        data = {'name': 'Malyn',
                'notification_interval': 6,
                'user': user2.id}
        self.client.post(url, data, format='json')

        url = '/api/v1/citydelete/2/'
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(City.objects.count(), 1)

    def test_user_logout(self):
        url = '/api/v1/auth/users/'
        data = {'username': 'user2',
                'password': 'mpzxqrbvsnpgkiwcss',
                'email': 'test12213@gmail.com'}
        self.client.post(url, data, format='json')
        self.client.login(username='user2', password='mpzxqrbvsnpgkiwcss')
        self.client.logout()

        user2 = User.objects.get(username='user2')

        url = '/api/v1/city/'
        data = {'name': 'Malyn',
                'notification_interval': 6,
                'user': user2.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.data['detail'], 'Authentication credentials were not provided.')
