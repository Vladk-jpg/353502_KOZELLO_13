from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile, Staff, calculate_age
from .forms import UserRegistrationForm
from datetime import date, timedelta

class AccountsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            role='client',
            phone_number='+375 (29) 123-45-67',
            birth_date=date(1990, 1, 1)
        )
        
        self.admin_user = User.objects.create_superuser(
            username='admin',
            password='admin123',
            email='admin@example.com'
        )
        
        self.agent_user = User.objects.create_user(
            username='agent',
            password='agent123',
            email='agent@example.com'
        )
        self.agent_profile = UserProfile.objects.create(
            user=self.agent_user,
            role='agent',
            phone_number='+375 (29) 765-43-21',
            birth_date=date(1985, 1, 1)
        )
        
        self.staff = Staff.objects.create(
            user_profile=self.agent_profile,
            position='Senior Agent',
            experience=5
        )

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 401)

    def test_register_view(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123',
            'phone_number': '+375 (29) 123-45-68',
            'birth_date': '01/01/1999'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        response = self.client.post(reverse('register'), {
            'username': 'invaliduser',
            'email': 'invalid@example.com',
            'password1': 'newpass123',
            'password2': 'newpass123',
            'phone_number': '1234567890',
            'birth_date': '1990-01-01'
        })
        self.assertEqual(response.status_code, 400)
        self.assertFalse(User.objects.filter(username='invaliduser').exists())

    def test_profile_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        
        self.client.logout()
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)

    def test_user_profile_creation(self):
        self.assertEqual(self.user_profile.role, 'client')
        self.assertEqual(self.user_profile.phone_number, '+375 (29) 123-45-67')
        self.assertEqual(str(self.user_profile.birth_date), '1990-01-01')
        
        self.assertEqual(self.user_profile.age(), 35)  

    def test_staff_creation(self):
        self.assertEqual(self.staff.position, 'Senior Agent')
        self.assertEqual(self.staff.experience, 5)
        self.assertTrue(self.staff.is_active)
        
        self.assertEqual(self.staff.user_profile, self.agent_profile)

    def test_underage_user(self):
        young_user = User.objects.create_user(username='younguser', password='pass123')
        birth_date = date.today() - timedelta(days=365*17 + 1)
        
        young_profile = UserProfile(
            user=young_user,
            role='client',
            phone_number='+375 (29) 123-45-67',
            birth_date=birth_date
        )
        
        with self.assertRaises(ValidationError):
            young_profile.full_clean()
            young_profile.save()
        
        self.assertFalse(UserProfile.objects.filter(user=young_user).exists())

    def test_user_following(self):
        self.user_profile.following.add(self.agent_profile)
        self.assertEqual(self.user_profile.following.count(), 1)
        self.assertEqual(self.agent_profile.clients.count(), 1)
        
        self.user_profile.following.remove(self.agent_profile)
        self.assertEqual(self.user_profile.following.count(), 0)
        self.assertEqual(self.agent_profile.clients.count(), 0)
