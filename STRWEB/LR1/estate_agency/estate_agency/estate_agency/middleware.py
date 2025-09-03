from django.utils import timezone

class UserTimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        if user.is_authenticated and hasattr(user, 'userprofile') and user.userprofile.timezone:
            timezone.activate(user.userprofile.timezone)
        else:
            timezone.deactivate()
        return self.get_response(request)
