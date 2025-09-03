import matplotlib
matplotlib.use('Agg') 

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from properties.models import Property
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
import matplotlib.pyplot as plt
import io
import base64
from sales.models import Sale
import numpy as np
from accounts.decorators import role_required
from .models import About, Article, FAQ, Vacancy, Review
from .forms import ReviewForm
import requests
from django.conf import settings
import calendar
import datetime


def get_client_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        if response.status_code == 200:
            return response.json()['ip']
    except:
        return 'Не удалось получить IP'
    return 'Не удалось получить IP'

def base_context(request):
    return {
        'client_ip': get_client_ip(),
        'tz': timezone.get_current_timezone()
    }

def home(request):
    latest_property = Property.objects.filter(status='available').first()
    
    today = datetime.date.today()
    current_date = today.strftime("%d %B %Y") 
    
    cal = calendar.TextCalendar()
    month_calendar = cal.formatmonth(today.year, today.month)
    
    context = {
        'latest_property': latest_property,
        'current_date': current_date, 
        'month_calendar': month_calendar, 
    }
    return render(request, 'content/home.html', context)

@role_required(['admin'])
def statistics_view(request):
    category_counts = Property.objects.values('category__name').annotate(count=Count('id'))
    
    plt.figure(figsize=(10, 6))
    plt.pie([item['count'] for item in category_counts], 
            labels=[item['category__name'] for item in category_counts],
            autopct='%1.1f%%')
    plt.title('Распределение недвижимости по категориям')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()
    
    graph = base64.b64encode(image_png).decode('utf-8')
    
    last_month = timezone.now() - timedelta(days=30)
    sales = Sale.objects.filter(
        sale_date__gte=last_month,
        status='approved'
    ).select_related('agent', 'agent__user', 'property')
    
    employee_stats = []
    for sale in sales:
        agent = sale.agent
        stat = next((s for s in employee_stats if s['agent'] == agent), None)
        if stat is None:
            stat = {
                'agent': agent,
                'agent_name': f"{agent.user.first_name} {agent.user.last_name}",
                'total_sales': 0,
                'total_amount': 0
            }
            employee_stats.append(stat)
        stat['total_sales'] += 1
        if (sale.promo):
            stat['total_amount'] += round(sale.property.price * (1 -sale.promo.discount_percentage / 100))
        else:
            stat['total_amount'] += round(sale.property.price)
    
    employee_stats.sort(key=lambda x: x['total_sales'], reverse=True)
    
    last_month_sales = [(sale.property.price * (1 - sale.promo.discount_percentage / 100) if sale.promo else sale.property.price) for sale in sales]
    
    if last_month_sales:
        sales_array = np.array(last_month_sales)
        mean_sales = np.mean(sales_array)
        median_sales = np.median(sales_array)
        mode_sales = float(np.bincount(sales_array.astype(int)).argmax())
    else:
        mean_sales = median_sales = mode_sales = 0
    
    context = {
        'property_distribution_graph': graph,
        'employee_stats': employee_stats,
        'mean_sales': round(mean_sales),
        'median_sales': round(median_sales),
        'mode_sales': round(mode_sales),
    }
    
    return render(request, 'content/statistics.html', context)

def about_view(request):
    about_info = About.objects.first()
    return render(request, 'content/about.html', {'about_info': about_info})

def news_view(request):
    articles = Article.objects.all()
    return render(request, 'content/news.html', {'articles': articles})

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'content/article_detail.html', {'article': article})

def faq_view(request):
    faqs = FAQ.objects.all()
    return render(request, 'content/faq.html', {'faqs': faqs})

def privacy_policy_view(request):
    return render(request, 'content/privacy_policy.html')

def vacancies_view(request):
    vacancies = Vacancy.objects.all()
    return render(request, 'content/vacancies.html', {'vacancies': vacancies})

def reviews_view(request):
    reviews = Review.objects.all()
    form = ReviewForm()
    return render(request, 'content/reviews.html', {
        'reviews': reviews,
        'form': form
    })

@login_required
@role_required(['client'])
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user_name = request.user.username
            review.save()
            messages.success(request, 'Ваш отзыв успешно добавлен!')
            return redirect('content:reviews')
    else:
        form = ReviewForm()
    return render(request, 'content/add_review.html', {'form': form})
