from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from api.models import OperatorCodeModel, Tag, TimeZoneModel, ClientModel
from django.utils import timezone
from django.test import TestCase, override_settings


@override_settings(CELERY_BROKER_URL='memory://localhost/')
class MyAPIViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.operator_code = OperatorCodeModel.objects.create(code="1")
        self.timezone = TimeZoneModel.objects.create(name="Test Zone", timezone="UTC")
        self.tag = Tag.objects.create(name="Test Tag")

    def test_client_viewset(self):
        data = {
            'phone_number': '1234567890',
            'operator_code': self.operator_code.id,
            'timezone': self.timezone.id,
            'tags': [self.tag.id],
        }
        response = self.client.post('/api/clients/', data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        client_id = response.data['id']

        response = self.client.get(f'/api/clients/{client_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {'phone_number': '1234234590'}
        response = self.client.patch(f'/api/clients/{client_id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # # Проверка обновления phone_number
        updated_client = ClientModel.objects.get(id=client_id)
        self.assertEqual(updated_client.phone_number, '1234234590')

        response = self.client.delete(f'/api/clients/{client_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_mailing_list_viewset(self):
        data = {
            'start_datetime': timezone.now(),
            'end_datetime': timezone.now(),
            'message': 'Test Message',
            'operator_code': self.operator_code.id,
            'tags': [self.tag.id],
        }
        response = self.client.post('/api/mailing_lists/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mailing_list_id = response.data['id']

        response = self.client.get(f'/api/mailing_lists/{mailing_list_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {'message': 'updated_message'}
        response = self.client.patch(f'/api/mailing_lists/{mailing_list_id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'updated_message')

        response = self.client.delete(f'/api/mailing_lists/{mailing_list_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_tag_viewset(self):
        data = {
            'name': 'new',
        }
        response = self.client.post('/api/tag/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        tag_id = response.data['id']

        response = self.client.get(f'/api/tag/{tag_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {'name': 'news'}
        response = self.client.patch(f'/api/tag/{tag_id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'news')

        response = self.client.delete(f'/api/tag/{tag_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    def test_timezone_viewset(self):
        data = {
            'name': 'Moscow',
            'timezone': 'UTC+1',
        }
        response = self.client.post('/api/timezone/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        timezone_id = response.data['id']

        response = self.client.get(f'/api/timezone/{timezone_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {'timezone': 'UTC+2'}
        response = self.client.patch(f'/api/timezone/{timezone_id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['timezone'], 'UTC+2')

        response = self.client.delete(f'/api/timezone/{timezone_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_operator_code_viewset(self):
        data = {
            'code': '925',
        }
        response = self.client.post('/api/operator_code/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        code_id = response.data['id']

        response = self.client.get(f'/api/operator_code/{code_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = {'code': '999'}
        response = self.client.patch(f'/api/operator_code/{code_id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['code'], '999')

        response = self.client.delete(f'/api/operator_code/{code_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

