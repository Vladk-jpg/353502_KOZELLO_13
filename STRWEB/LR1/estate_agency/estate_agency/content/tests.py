from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import About, Article, FAQ, Vacancy, Review
from .forms import ReviewForm
from accounts.models import UserProfile
from datetime import date, timedelta
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError

class ContentTests(TestCase):
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
        
        self.about = About.objects.create(
            company_info='Test company information'
        )
        
        self.test_image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'',
            content_type='image/jpeg'
        )
        
        self.article1 = Article.objects.create(
            title='Test Article 1',
            content='Test content 1',
            image=self.test_image,
            created_at=date.today()
        )
        
        self.article2 = Article.objects.create(
            title='Test Article 2',
            content='Test content 2' * 100, 
            image=self.test_image,
            created_at=date.today() - timedelta(days=1)
        )
        
        self.faq1 = FAQ.objects.create(
            question='Test Question 1',
            answer='Test Answer 1'
        )
        
        self.faq2 = FAQ.objects.create(
            question='Test Question 2',
            answer='Test Answer 2'
        )
        
        self.vacancy1 = Vacancy.objects.create(
            title='Test Vacancy 1',
            description='Test description 1'
        )
        
        self.vacancy2 = Vacancy.objects.create(
            title='Test Vacancy 2',
            description='Test description 2'
        )
        
        self.review1 = Review.objects.create(
            user_name='Test User 1',
            rating=5,
            text='Test review 1'
        )
        
        self.review2 = Review.objects.create(
            user_name='Test User 2',
            rating=3,
            text='Test review 2'
        )

    def test_about_view(self):
        response = self.client.get(reverse('content:about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'content/about.html')
        self.assertContains(response, 'Test company information')

    def test_news_view(self):
        response = self.client.get(reverse('content:news'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'content/news.html')
        self.assertContains(response, 'Test Article 1')
        self.assertContains(response, 'Test Article 2')

    def test_article_detail_view(self):
        response = self.client.get(reverse('content:article_detail', args=[self.article1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'content/article_detail.html')
        self.assertContains(response, 'Test Article 1')
        self.assertContains(response, 'Test content 1')
        
        response = self.client.get(reverse('content:article_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_article_short_content(self):
        self.assertEqual(len(self.article1.get_short_content()), len(self.article1.content))
        self.assertTrue(self.article2.get_short_content().endswith('...'))
        self.assertEqual(len(self.article2.get_short_content()), 203)

    def test_faq_view(self):
        response = self.client.get(reverse('content:faq'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'content/faq.html')
        self.assertContains(response, 'Test Question 1')
        self.assertContains(response, 'Test Question 2')
        self.assertContains(response, 'Test Answer 1')
        self.assertContains(response, 'Test Answer 2')

    def test_vacancies_view(self):
        response = self.client.get(reverse('content:vacancies'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'content/vacancies.html')
        self.assertContains(response, 'Test Vacancy 1')
        self.assertContains(response, 'Test Vacancy 2')

    def test_reviews_view(self):
        response = self.client.get(reverse('content:reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'content/reviews.html')
        self.assertContains(response, 'Test review 1')
        self.assertContains(response, 'Test review 2')
        self.assertContains(response, '5')
        self.assertContains(response, '3')

    def test_add_review_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('content:add_review'), {
            'user_name': self.user_profile.user.username,
            'rating': 4,
            'text': 'New test review'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(text='New test review').exists())
        
        response = self.client.post(reverse('content:add_review'), {
            'user_name': self.user_profile.user.username,
            'rating': 11,
            'text': 'Invalid review'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Review.objects.filter(text='Invalid review').exists())
        
        self.client.logout()
        response = self.client.post(reverse('content:add_review'), {
            'user_name': 'Test User 5',
            'rating': 5,
            'text': 'Unauthorized review'
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(text='Unauthorized review').exists())

    def test_review_form(self):
        form_data = {
            'user_name': 'Test User',
            'rating': 5,
            'text': 'Test review form'
        }
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        form_data['rating'] = 11
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        
        form_data['rating'] = 5
        form_data['text'] = ''
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_article_creation(self):
        self.assertEqual(self.article1.title, 'Test Article 1')
        self.assertEqual(self.article1.content, 'Test content 1')
        
        self.article1.title = 'Updated Title'
        self.article1.save()
        self.assertEqual(Article.objects.get(id=self.article1.id).title, 'Updated Title')

    def test_vacancy_creation(self):
        self.assertEqual(self.vacancy1.title, 'Test Vacancy 1')
        self.assertEqual(self.vacancy1.description, 'Test description 1')
        
        self.vacancy1.title = 'Updated Vacancy'
        self.vacancy1.save()
        self.assertEqual(Vacancy.objects.get(id=self.vacancy1.id).title, 'Updated Vacancy')

    def test_review_rating_validation(self):
        with self.assertRaises(ValidationError):
            review = Review(
                user_name='Test User',
                rating=11,
                text='Invalid review'
            )
            review.full_clean()
        
        with self.assertRaises(ValidationError):
            review = Review(
                user_name='Test User',
                rating=0,
                text='Invalid review'
            )
            review.full_clean()
