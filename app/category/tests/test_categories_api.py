from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Category
from category.serializers import CategorySerializer

CATEGORY_URL = reverse('category:category-list')

def detail_url(category_id):
    return reverse('category:category-detail', args=[category_id])

class PublicCategoriesAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_retrieve_categories(self):
        Category.objects.create(name='Delivery')
        Category.objects.create(name='Pickup')

        response = self.client.get(CATEGORY_URL)

        categories = Category.objects.all().order_by('name')
        serializer = CategorySerializer(categories, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_categories(self):
        payload = {
            'name': 'Food'
        }
        response = self.client.post(CATEGORY_URL, payload)

        category = Category.objects.get(id=response.data['id'])

        self.assertEqual(getattr(category, 'name'), payload['name'])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_category(self):
        category = Category.objects.create(name='Refrigerator')

        payload = {'name': 'Heating'}
        url = detail_url(category.id)
        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category.refresh_from_db()
        self.assertEqual(category.name, payload['name'])

    def test_delete_category(self):
        category = Category.objects.create(name='Food')

        url = detail_url(category.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(id=category.id).exists())