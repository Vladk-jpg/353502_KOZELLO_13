from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Для доступа к этой странице необходимо войти в систему.')
                return redirect('login')
            
            try:
                user_role = request.user.userprofile.role
                if user_role not in allowed_roles:
                    messages.error(request, 'У вас нет прав для доступа к этой странице.')
                    return redirect('home')
            except:
                messages.error(request, 'Профиль пользователя не найден.')
                return redirect('home')
                
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator 