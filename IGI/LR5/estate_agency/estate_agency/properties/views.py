from django.forms import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from .models import Property, Category
from .forms import PropertyForm, ReservationForm
from sales.models import Sale, Promo
from datetime import date, datetime
from django.utils import timezone
from accounts.forms import date_validator

def index(request):
    properties = Property.objects.filter(status='available')
    categories = Category.objects.all()
    
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    category_id = request.GET.get('category')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if min_price:
        properties = properties.filter(price__gte=min_price)
    if max_price:
        properties = properties.filter(price__lte=max_price)
    if category_id:
        properties = properties.filter(category_id=category_id)
    if date_from:
        try:
            date_validator(date_from)
            parsed_date_from = datetime.strptime(date_from, '%d/%m/%Y')
            properties = properties.filter(created_at__gte=parsed_date_from)
        except ValidationError:
            messages.error(request, 'Дата "от" должна быть в формате ДД/ММ/ГГГГ')

    if date_to:
        try:
            date_validator(date_to)
            parsed_date_to = datetime.strptime(date_to, '%d/%m/%Y')
            properties = properties.filter(created_at__lte=parsed_date_to)
        except ValidationError:
            messages.error(request, 'Дата "до" должна быть в формате ДД/ММ/ГГГГ')
    
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
    for category in categories:
        category.property_count = Property.objects.filter(category=category, status='available').count()
    
    context = {
        'categories': categories,
    }
    return render(request, 'properties/category_list.html', context)

@login_required
@role_required(['agent', 'admin'])
def agent_property_list(request):
    properties = Property.objects.filter(status='available')
    return render(request, 'properties/agent_property_list.html', {'properties': properties})

@login_required
@role_required(['agent', 'admin'])
def agent_property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property = form.save(commit=False)
            property.save()
            messages.success(request, 'Объект недвижимости успешно создан.')
            return redirect('agent_property_list')
    else:
        form = PropertyForm()
    return render(request, 'properties/agent_property_form.html', {'form': form, 'action': 'Создать'})

@login_required
@role_required(['agent', 'admin'])
def agent_property_edit(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property)
        if form.is_valid():
            form.save()
            messages.success(request, 'Объект недвижимости успешно обновлен.')
            return redirect('agent_property_list')
    else:
        form = PropertyForm(instance=property)
    return render(request, 'properties/agent_property_form.html', {'form': form, 'action': 'Редактировать'})

@login_required
@role_required(['agent', 'admin'])
def agent_property_delete(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        property.delete()
        messages.success(request, 'Объект недвижимости успешно удален.')
        return redirect('agent_property_list')
    return render(request, 'properties/agent_property_confirm_delete.html', {'property': property})

@login_required
@role_required(['client', 'admin'])
def property_reserve(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    
    if property.status != 'available':
        messages.error(request, 'Этот объект недвижимости уже забронирован или продан.')
        return redirect('property_detail', property_id=property_id)
    
    following_agents = request.user.userprofile.following.filter(role='agent')
    if not following_agents.exists():
        messages.error(request, 'У вас нет привязанного агента. Пожалуйста, свяжитесь с агентом для бронирования.')
        return redirect('property_detail', property_id=property_id)
    
    agent = following_agents.first()
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            promo_code = form.cleaned_data.get('promo_code')
            promo = None
            
            if promo_code:
                try:
                    promo = Promo.objects.get(promo_code=promo_code)
                    if promo.expires_at < timezone.now():
                        messages.error(request, 'Срок действия промокода истек.')
                        return redirect('property_detail', property_id=property_id)
                except Promo.DoesNotExist:
                    messages.error(request, 'Неверный промокод.')
                    return redirect('property_detail', property_id=property_id)
            
            sale = Sale.objects.create(
                client=request.user.userprofile,
                agent=agent,
                property=property,
                promo=promo,
                sale_date=None,
                contract_date=timezone.now(),
                status='pending'
            )
            
            property.status = 'reserved'
            property.save()
            
            messages.success(request, 'Объект недвижимости успешно забронирован.')
            return redirect('property_detail', property_id=property_id)
    else:
        form = ReservationForm()
    
    return render(request, 'properties/property_reserve.html', {
        'property': property,
        'form': form
    })

@login_required
@role_required(['client'])
def client_purchases(request):
    purchases = Sale.objects.filter(client=request.user.userprofile, status='approved').select_related('property', 'agent', 'promo')
    
    context = {
        'purchases': purchases,
    }
    return render(request, 'properties/client_purchases.html', context)

@login_required
@role_required(['agent'])
def agent_sales(request):
    sales = Sale.objects.filter(agent=request.user.userprofile).select_related('client', 'property', 'promo')
    
    if request.method == 'POST':
        sale_id = request.POST.get('sale_id')
        action = request.POST.get('action')
        
        if sale_id and action:
            sale = get_object_or_404(Sale, id=sale_id, agent=request.user.userprofile)
            
            if action == 'approve':
                sale.status = 'approved'
                sale.sale_date = date.today()
                sale.save()
                
                sale.property.status = 'sold'
                sale.property.save()
                
                messages.success(request, 'Продажа успешно подтверждена.')
            elif action == 'reject':
                sale.status = 'rejected'
                sale.save()
                
                sale.property.status = 'available'
                sale.property.save()
                
                messages.success(request, 'Заявка на покупку отклонена.')
            
            return redirect('agent_sales')
    
    context = {
        'sales': sales,
    }
    return render(request, 'properties/agent_sales.html', context)

@login_required
@role_required(['admin'])
def admin_sales(request):
    sales = Sale.objects.all().select_related('client', 'property', 'promo', 'agent')
    
    if request.method == 'POST':
        sale_id = request.POST.get('sale_id')
        action = request.POST.get('action')
        
        if sale_id and action:
            sale = get_object_or_404(Sale, id=sale_id)
            
            if action == 'approve':
                sale.status = 'approved'
                sale.sale_date = date.today()
                sale.save()
                
                sale.property.status = 'sold'
                sale.property.save()
                
                messages.success(request, 'Продажа успешно подтверждена.')
            elif action == 'reject':
                sale.status = 'rejected'
                sale.save()
                
                sale.property.status = 'available'
                sale.property.save()
                
                messages.success(request, 'Заявка на покупку отклонена.')
            
            return redirect('admin_sales')
    
    context = {
        'sales': sales,
    }
    return render(request, 'properties/admin_sales.html', context)

def promo_codes(request):
    today = timezone.now()
    
    active_promos = Promo.objects.filter(expires_at__gte=today).order_by('expires_at')
    expired_promos = Promo.objects.filter(expires_at__lt=today).order_by('-expires_at')

    context = {
        'active_promos': active_promos,
        'expired_promos': expired_promos,
    }
    return render(request, 'properties/promo_codes.html', context)
