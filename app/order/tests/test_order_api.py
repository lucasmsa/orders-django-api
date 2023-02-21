from datetime import date
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Order, Category
from order.serializers import (
    OrderSerializer,
    OrderDetailSerializer,
)

ORDERS_URL = reverse('order:order-list')

def detail_url(order_id):
    return reverse('order:order-detail', args=[order_id])

def create_user(**params):
    return get_user_model().objects.create_user(**params)

def create_category(**params):
    defaults = {
        'name': 'Delivery Category'
    }

    defaults.update(params)

    category = Category.objects.create(**defaults)
    return category

def create_order(user, **params):
    defaults = {
        'contact_name': 'Contact Name',
        'contact_phone': '839913829147',
        'description': 'Test description',
        'real_state_agency': 'Test real state agency',
        'company': 'Sato Company',
        'deadline': date(2025, 1, 1),
        'category': create_category(),
    }

    defaults.update(params)

    order = Order.objects.create(user=user, **defaults)
    return order

class PublicOrderAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(ORDERS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateOrderAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(email='user@example.com', password='tests123')
        self.client.force_authenticate(self.user)

    def test_retrieve_orders(self):
        for _ in range(5):
            create_order(user=self.user)

        response = self.client.get(ORDERS_URL)
        orders = Order.objects.all().order_by('-id')
        serializer = OrderSerializer(orders, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_orders_list_limited_to_user(self):
        other_user = create_user(
            email='other@example.com',
            password='testpass123'
        )
        create_order(user=other_user)
        create_order(user=self.user)

        response = self.client.get(ORDERS_URL)

        orders = Order.objects.filter(user=self.user)
        serializer = OrderSerializer(orders, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_order_detail(self):
        order = create_order(user=self.user)

        url = detail_url(order.id)
        response = self.client.get(url)

        serializer = OrderDetailSerializer(order)
        self.assertEqual(response.data, serializer.data)

    def test_create_order(self):
        category = create_category(name='Truck')
        payload = {
            'contact_name': 'Contactor',
            'contact_phone': '839913324234',
            'description': 'Descripciones',
            'real_state_agency': 'Sigma',
            'company': 'Arasaka',
            'deadline': date(2024, 2, 3),
            'category': {'name': category.name},
        }

        response = self.client.post(ORDERS_URL, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(id=response.data['id'])

        for key, value in payload.items():
            if key != 'category':
                self.assertEqual(getattr(order, key), value)

        self.assertEqual(order.user, self.user)
        self.assertEqual(order.category.name, payload['category']['name'])

    def test_deadline_cannot_be_in_the_past(self):
        payload = {
            'contact_name': 'Contactor',
            'contact_phone': '839913324234',
            'description': 'Descripciones',
            'real_state_agency': 'Omega',
            'company': 'Arasaka',
            'deadline': date(2010, 2, 3),
            'category': create_category(),
        }

        response = self.client.post(ORDERS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_phone_must_be_valid(self):
        payload = {
            'contact_name': 'Contactor',
            'contact_phone': 'invalid phone',
            'description': 'Descripciones',
            'real_state_agency': 'Dunder Mifflin',
            'company': 'Arasaka',
            'deadline': date(2010, 2, 3),
            'category': create_category(),
        }

        response = self.client.post(ORDERS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_partial_updated(self):
        original_deadline = date(2024, 2, 3)
        order = create_order(
            user=self.user,
            contact_name='Contactor',
            contact_phone='839913324234',
            description='Descriptones',
            real_state_agency='Gearbox',
            company='Militech',
            deadline=original_deadline,
            category=create_category()
        )
        payload = {
            'contact_name': 'Little contact',
        }
        url = detail_url(order.id)

        response = self.client.patch(url, payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        self.assertEqual(order.contact_name, payload['contact_name'])
        self.assertEqual(order.deadline, original_deadline)
        self.assertEqual(order.user, self.user)

    def test_full_update(self):
        order = create_order(
            user=self.user,
            description='Descriptar',
            contact_name='contact',
            contact_phone='83912444234',
            real_state_agency='Akira',
            company='Toryama',
            deadline=date(2024, 2, 3),
            category=create_category(name='Movies')
        )

        payload = {
            'contact_name': 'Contactor',
            'contact_phone': '8391242356',
            'description': 'Describing',
            'real_state_agency': 'Rasputin',
            'company': 'Machine',
            'deadline': date(2026, 2, 3),
            'category': {'name': 'Cargo'},
        }

        url = detail_url(order.id)
        response = self.client.put(url, payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        order.refresh_from_db()
        for key, value in payload.items():
            if key != 'category':
                self.assertEqual(getattr(order, key), value)

        self.assertEqual(order.user, self.user)
        self.assertEqual(order.category.name, payload['category']['name'])

    def test_update_user_returns_error(self):
        new_user = create_user(email='another_user@example.com', password='pass123')
        order = create_order(user=self.user)

        payload = {'user': new_user.id}

        url = detail_url(order.id)

        self.client.patch(url, payload)

        order.refresh_from_db()
        self.assertEqual(order.user, self.user)

    def test_delete_order(self):
        order = create_order(user=self.user)

        url = detail_url(order.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(id=order.id).exists())

    def test_delete_other_users_order_returns_error(self):
        other_user = create_user(email='other@example.com', password='pass123')
        order = create_order(user=other_user)

        url = detail_url(order.id)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Order.objects.filter(id=order.id).exists())


