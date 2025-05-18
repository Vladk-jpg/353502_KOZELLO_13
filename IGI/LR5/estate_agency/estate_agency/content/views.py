import matplotlib
matplotlib.use('Agg') 

from django.shortcuts import render
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


def home(request):
    latest_property = Property.objects.filter(status='available').first()
    context = {
        'latest_property': latest_property
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
        stat['total_amount'] += sale.property.price
    
    employee_stats.sort(key=lambda x: x['total_sales'], reverse=True)
    
    last_month_sales = [sale.property.price for sale in sales]
    
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
        'mean_sales': round(mean_sales, 2),
        'median_sales': round(median_sales, 2),
        'mode_sales': round(mode_sales, 2),
    }
    
    return render(request, 'content/statistics.html', context)
