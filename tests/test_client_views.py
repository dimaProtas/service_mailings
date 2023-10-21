from django.test import TestCase
from django.urls import reverse
from api.models import OperatorCodeModel, Tag

class YourViewTest(TestCase):
    def setUp(self):
        # Создайте необходимые объекты в базе данных перед тестами
        self.operator_code = OperatorCodeModel.objects.create(code="123")
        self.tag = Tag.objects.create(name="Test Tag")

    def test_client_view(self):
        response = self.client.get(reverse('client'))
        self.assertEqual(response.status_code, 200)  # Проверяем, что ответ успешный

    def test_operator_code_view(self):
        response = self.client.get(reverse('operator_cods'))
        self.assertEqual(response.status_code, 200)  # Проверяем, что ответ успешный

    def test_operator_code_create(self):
        response = self.client.post(reverse('operator_cods'), data={'code': '456'})
        self.assertEqual(response.status_code, 200)  # Проверяем, что ответ успешный

    def test_operator_code_delete(self):
        code = OperatorCodeModel.objects.create(code="789")
        response = self.client.post(reverse('operator_code_delete', args=[code.id]))
        self.assertEqual(response.status_code, 302)  # Проверяем, что произошел редирект
