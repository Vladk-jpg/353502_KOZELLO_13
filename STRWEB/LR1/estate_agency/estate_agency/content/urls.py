from django.urls import path, re_path
from . import views

app_name = 'content'

urlpatterns = [
    path('', views.home, name='home'),
    path('statistics/', views.statistics_view, name='statistics'),
    path('about/', views.about_view, name='about'),
    path('news/', views.news_view, name='news'),
    path('news/<int:article_id>/', views.article_detail, name='article_detail'),
    path('faq/', views.faq_view, name='faq'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    path('date-manipulation/', views.date_manipulation_view, name='date_manipulation'),
    path('charts/', views.charts_view, name='charts'),
    re_path(r'^vacancies/?$', views.vacancies_view, name='vacancies'),
    path('reviews/', views.reviews_view, name='reviews'),
    path('reviews/add/', views.add_review, name='add_review'),
] 