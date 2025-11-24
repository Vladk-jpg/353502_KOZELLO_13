from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegistrationForm, StaffForm
from django.http import HttpResponse
from .decorators import role_required
from .models import UserProfile, Staff
import random
import requests
import json
from datetime import datetime
from django.http import JsonResponse
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_profile = UserProfile.objects.get(user=user)
            
            if user_profile.role == 'client':
                agents = UserProfile.objects.filter(role='agent')
                if agents.exists():
                    random_agent = random.choice(list(agents))
                    user_profile.following.add(random_agent)
                    messages.success(request, f'Вам назначен агент: {random_agent.user.get_full_name() or random_agent.user.username}')
            
            login(request, user)
            messages.success(request, 'Регистрация успешно завершена!')
            return redirect('/accounts/profile')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
            return render(request, 'accounts/register.html', {'form': form}, status=400)
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/accounts/profile')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
            return render(request, 'accounts/login.html', status=401)
    return render(request, 'accounts/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из системы.')
    return redirect('/properties/')

def get_random_dog():
    try:
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        if response.status_code == 200:
            return response.json()['message']
    except:
        return None
    return None

@login_required
def profile_view(request):
    user_profile = request.user.userprofile
    context = {}
    
    if user_profile.role == 'client':
        agent = user_profile.following.filter(role='agent').first()
        if agent:
            context['agent'] = agent
    elif user_profile.role == 'agent':
        clients = user_profile.clients.all()
        context['clients'] = clients
    
    context['dog_image'] = get_random_dog()
    return render(request, 'accounts/profile.html', context)

def staff_list(request):
    staff_members = Staff.objects.filter(is_active=True)
    return render(request, 'accounts/staff_list.html', {'staff_members': staff_members})

@login_required
@role_required(['admin'])
def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сотрудник успешно добавлен!')
            return redirect('staff_list')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = StaffForm()
    return render(request, 'accounts/add_staff.html', {'form': form})

def staff_list_api(request):
    staff_members = Staff.objects.filter(is_active=True).select_related('user_profile__user')
    data = []
    for staff in staff_members:
        data.append({
            'id': staff.id,
            'name': staff.user_profile.user.get_full_name() or staff.user_profile.user.username,
            'position': staff.position,
            'experience': staff.experience,
            'email': staff.user_profile.user.email,
            'phone': staff.user_profile.phone_number,
            'photo_url': staff.photo.url if staff.photo else None
        })
    return JsonResponse({'staff': data}, safe=False)

@csrf_exempt
@require_http_methods(["POST"])
@login_required
@role_required(['admin'])
def add_staff_api(request):
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST.dict()
        
        birth_date = datetime.strptime(data['birth_date'], '%d/%m/%Y').date()
        
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', '')
        )
        
        user_profile = UserProfile.objects.create(
            user=user,
            role='agent',
            phone_number=data['phone_number'],
            birth_date=birth_date,
            timezone=data.get('timezone', 'Europe/Moscow')
        )
        
        staff = Staff.objects.create(
            user_profile=user_profile,
            position=data['position'],
            experience=int(data['experience']),
            is_active=True
        )
        
        if 'photo' in request.FILES:
            staff.photo = request.FILES['photo']
            staff.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Success!',
            'staff': {
                'id': staff.id,
                'name': user.get_full_name() or user.username,
                'position': staff.position,
                'experience': staff.experience,
                'email': user.email,
                'phone': user_profile.phone_number,
                'photo_url': staff.photo.url if staff.photo else None
            }
        }, status=201)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
