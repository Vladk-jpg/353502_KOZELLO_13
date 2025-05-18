from django.urls import path
from . import views

app_name = 'content'

urlpatterns = [
    path('', views.home, name='home'),
    path('statistics/', views.statistics_view, name='statistics'),
] 