from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Property, Category

def index(request):
    properties = Property.objects.all()
    categories = Category.objects.all()
    
    # Get filter parameters
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    category_id = request.GET.get('category')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    # Apply filters
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)
    if category_id:
        properties = properties.filter(category_id=category_id)
    if date_from:
        properties = properties.filter(created_at__gte=date_from)
    if date_to:
        properties = properties.filter(created_at__lte=date_to)
    
    context = {
        'properties': properties,
        'categories': categories,
        'current_filters': {
            'min_price': min_price,
            'max_price': max_price,
            'category_id': category_id,
            'date_from': date_from,
            'date_to': date_to,
        }
    }
    
    return render(request, 'properties/index.html', context)

def property_detail(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    related_properties = Property.objects.filter(
        category=property.category
    ).exclude(id=property_id)[:3] 
    
    context = {
        'property': property,
        'related_properties': related_properties,
    }
    return render(request, 'properties/property_detail.html', context)

def category_list(request):
    categories = Category.objects.all()
    # Get count of properties for each category
    for category in categories:
        category.property_count = Property.objects.filter(category=category).count()
    
    context = {
        'categories': categories,
    }
    return render(request, 'properties/category_list.html', context)
