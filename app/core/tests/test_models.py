from datetime import date
from django.test import TestCase
from core import models
from django.contrib.auth import get_user_model

def create_category(**params):
    defaults = {
        'name': 'Delivery Category'
    }

    defaults.update(params)

    category = models.Category.objects.create(**defaults)
    return category

class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        email = "test@example.com"
        password = "testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        example_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['test2@ExAmple.Com', 'test2@example.com'],
            ['Test3@EXAMPLE.COM', 'Test3@example.com']
        ]

        for email, expected in example_emails:
            user = get_user_model().objects.create_user(email, 'test123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')


    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_order(self):
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )

        order = models.Order.objects.create(
            user=user,
            contact_name='Contact Name',
            contact_phone='839913829147',
            description='Test description',
            real_state_agency='Test real state agency',
            company='Sato Company',
            deadline=date(2025, 1, 1),
            category=models.Category.objects.create(name='Test Category'),
        )

        self.assertEqual(str(order), order.description)

    def test_create_category(self):
        category = models.Category.objects.create(name='Test Category')
        self.assertEqual(str(category), category.name)