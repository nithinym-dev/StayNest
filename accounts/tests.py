from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import User, OwnerProfile
from .forms import UserRegistrationForm, OwnerRegistrationForm

class AccountsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            user_type='user'
        )
        self.owner = User.objects.create_user(
            username='testowner',
            password='testpass123',
            email='owner@example.com',
            user_type='owner'
        )

    def test_user_registration(self):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'phone_number': '1234567890',
            'user_type': 'user',
            'password1': 'complex_password123',
            'password2': 'complex_password123',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_owner_registration(self):
        self.client.login(username='testowner', password='testpass123')
        with open('media/property_images/unnamed.jpg', 'rb') as f:
            image = SimpleUploadedFile("test.jpg", f.read(), content_type="image/jpeg")
        data = {
            'document_type': 'pan',
            'document_number': 'ABC123',
            'document_image': image,
            'business_name': 'Test Business',
            'business_address': 'Test Address',
        }
        response = self.client.post(reverse('owner_register'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(OwnerProfile.objects.filter(user=self.owner).exists())

    def test_login_and_logout(self):
        # Test login
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)

        # Test logout
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_dashboard_access(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_profile_update(self):
        self.client.login(username='testuser', password='testpass123')
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '9876543210',
        }
        response = self.client.post(reverse('profile'), data)
        self.assertEqual(response.status_code, 302)
        updated_user = User.objects.get(username='testuser')
        self.assertEqual(updated_user.first_name, 'Test')
        self.assertEqual(updated_user.last_name, 'User')
        self.assertEqual(updated_user.phone_number, '9876543210')
