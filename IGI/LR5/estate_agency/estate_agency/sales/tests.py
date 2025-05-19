from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Sale, Promo
from properties.models import Property, Category
from accounts.models import UserProfile
from datetime import date, timedelta

class SalesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.agent_user = User.objects.create_user(
            username='agent',
            password='agent123',
            email='agent@example.com'
        )
        self.agent = UserProfile.objects.create(
            user=self.agent_user,
            role='agent',
            birth_date=date(1990, 1, 1),
            phone_number='+375 (29) 123-45-67',
            timezone='UTC',
        )
        
        self.client_user = User.objects.create_user(
            username='client',
            password='client123',
            email='client@example.com'
        )
        self.client_profile = UserProfile.objects.create(
            user=self.client_user,
            role='client',
            birth_date=date(1990, 1, 1),
            phone_number='+375 (29) 765-43-21',
            timezone='UTC'
        )
        
        self.category = Category.objects.create(
            name='Test Category',
            description='Test description'
        )
        self.property1 = Property.objects.create(
            title='Test Property 1',
            description='Test description 1',
            price=100000,
            category=self.category,
            status='available'
        )
        self.property2 = Property.objects.create(
            title='Test Property 2',
            description='Test description 2',
            price=200000,
            category=self.category,
            status='available'
        )
        
        self.promo1 = Promo.objects.create(
            promo_code='SUMMER2025',
            discount_percentage=10,
            expires_at=timezone.now() + timedelta(days=30)
        )
        self.promo2 = Promo.objects.create(
            promo_code='WINTER2025',
            discount_percentage=20,
            expires_at=timezone.now() - timedelta(days=1)
        )
        
        self.sale1 = Sale.objects.create(
            property=self.property1,
            agent=self.agent,
            client=self.client_profile,
            sale_date=timezone.now().date(),
            contract_date=timezone.now().date(),
            status='pending'
        )
        self.sale2 = Sale.objects.create(
            property=self.property2,
            agent=self.agent,
            client=self.client_profile,
            sale_date=timezone.now().date(),
            contract_date=timezone.now().date(),
            status='approved',
            promo=self.promo1
        )

    def test_sale_creation(self):
        self.assertEqual(self.sale1.property, self.property1)
        self.assertEqual(self.sale1.agent, self.agent)
        self.assertEqual(self.sale1.client, self.client_profile)
        self.assertEqual(self.sale1.status, 'pending')
        
        self.assertEqual(self.sale2.promo, self.promo1)
        self.assertEqual(self.sale2.get_final_price(), 180000)

    def test_client_purchases_view(self):
        self.client.login(username='client', password='client123')
        response = self.client.get(reverse('client_purchases'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'properties/client_purchases.html')
        self.assertContains(response, 'Test Property 1')
        self.assertContains(response, 'Test Property 2')
        
        self.client.logout()
        response = self.client.get(reverse('client_purchases'))
        self.assertEqual(response.status_code, 302)

    def test_agent_sales_view(self):
        self.client.login(username='agent', password='agent123')
        response = self.client.get(reverse('agent_sales'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'properties/agent_sales.html')
        self.assertContains(response, 'Test Property 1')
        self.assertContains(response, 'Test Property 2')
        
        self.client.logout()
        response = self.client.get(reverse('agent_sales'))
        self.assertEqual(response.status_code, 302)

    def test_sale_status_changes(self):
        self.sale1.status = 'approved'
        self.sale1.save()
        self.assertEqual(Sale.objects.get(id=self.sale1.id).status, 'approved')
        
        self.sale1.status = 'rejected'
        self.sale1.save()
        self.assertEqual(Sale.objects.get(id=self.sale1.id).status, 'rejected')

    def test_sale_dates(self):
        future_date = timezone.now().date() + timedelta(days=30)
        self.sale1.sale_date = future_date
        self.sale1.save()
        self.assertEqual(Sale.objects.get(id=self.sale1.id).sale_date.date(), future_date)

        contract_date = timezone.now().date() + timedelta(days=7)
        self.sale1.contract_date = contract_date
        self.sale1.save()
        self.assertEqual(Sale.objects.get(id=self.sale1.id).contract_date.date(), contract_date)

    def test_sale_string_representation(self):
        self.assertEqual(str(self.sale1), f'Продажа {self.client_profile} - {self.sale1.sale_date}')
        self.assertEqual(str(self.sale2), f'Продажа {self.client_profile} - {self.sale2.sale_date}')

    def test_promo_string_representation(self):
        self.assertEqual(str(self.promo1), 'SUMMER2025 - 10%')
        self.assertEqual(str(self.promo2), 'WINTER2025 - 20%')
