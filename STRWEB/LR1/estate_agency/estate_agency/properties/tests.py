from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Property, Category
from accounts.models import UserProfile
from datetime import date
from django.core.exceptions import ValidationError

class PropertiesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            role='agent',
            phone_number='+375 (29) 123-45-67',
            birth_date=date(1990, 1, 1)
        )
        
        self.category1 = Category.objects.create(
            name='Apartments',
            description='Apartment properties'
        )
        self.category2 = Category.objects.create(
            name='Houses',
            description='House properties'
        )
        
        self.property1 = Property.objects.create(
            title='Luxury Apartment',
            description='Beautiful apartment in city center',
            price=150000,
            category=self.category1,
            status='available'
        )
        
        self.property2 = Property.objects.create(
            title='Family House',
            description='Spacious family house with garden',
            price=250000,
            category=self.category2,
            status='reserved'
        )

    def test_property_list_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'properties/index.html')

    def test_property_detail_view(self):
        response = self.client.get(reverse('property_detail', args=[self.property1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'properties/property_detail.html')
        self.assertContains(response, 'Luxury Apartment')
        self.assertContains(response, '150000')
        
        response = self.client.get(reverse('property_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_category_list_view(self):
        response = self.client.get(reverse('category_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'properties/category_list.html')
        self.assertContains(response, 'Apartments')
        self.assertContains(response, 'Houses')

    def test_property_filter(self):
        response = self.client.get(reverse('index'), {'category': self.category1.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Luxury Apartment') 
        self.assertNotContains(response, 'Family House') 

        response = self.client.get(reverse('index'), {
            'category': self.category2.id,
            'min_price': 200000,
            'max_price': 300000,
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Luxury Apartment')     
        
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Luxury Apartment')

    def test_property_creation(self):
        self.assertEqual(self.property1.title, 'Luxury Apartment')
        self.assertEqual(self.property1.price, 150000)
        self.assertEqual(self.property1.category, self.category1)
        self.assertEqual(self.property1.status, 'available')
        
        property3 = Property.objects.create(
            title='Minimal Property',
            price=100000,
            category=self.category1
        )
        self.assertEqual(property3.description, '')
        self.assertEqual(property3.status, 'available')

    def test_category_creation(self):
        self.assertEqual(self.category1.name, 'Apartments')
        self.assertEqual(self.category1.description, 'Apartment properties')
        
        category3 = Category.objects.create(name='Land')
        self.assertEqual(category3.description, '')

    def test_property_status_changes(self):
        self.property1.status = 'reserved'
        self.property1.save()
        self.assertEqual(Property.objects.get(id=self.property1.id).status, 'reserved')
        
        self.property1.status = 'sold'
        self.property1.save()
        self.assertEqual(Property.objects.get(id=self.property1.id).status, 'sold')

    def test_property_price_updates(self):
        self.property1.price = 160000
        self.property1.full_clean()
        self.property1.save()
        self.assertEqual(Property.objects.get(id=self.property1.id).price, 160000)
        
        self.property1.price = 0
        self.property1.full_clean()
        self.property1.save()
        self.assertEqual(Property.objects.get(id=self.property1.id).price, 0)
        
        with self.assertRaises(ValidationError):
            self.property1.price = -1000
            self.property1.full_clean()
            self.property1.save()

    def test_property_string_representation(self):
        self.assertEqual(str(self.property1), 'Luxury Apartment (150000 BYN)')
        self.assertEqual(str(self.property2), 'Family House (250000 BYN)')

    def test_category_string_representation(self):
        self.assertEqual(str(self.category1), 'Apartments')
        self.assertEqual(str(self.category2), 'Houses')
