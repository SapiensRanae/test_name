from django.shortcuts import redirect
from django.urls import resolve, Resolver404
from django.conf import settings

from django.shortcuts import redirect
from django.urls import resolve, Resolver404

EXEMPT_URLS = [
    'login',
    'logout',
    'index',

    'about_project',

    'login',
    'logout',
    'register',
    'welcome',

    'creator'
]


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            resolver_match = resolve(request.path)
            view_name = resolver_match.view_name
        except Resolver404:
            return self.get_response(request)

        # Дозволені URL
        if view_name in EXEMPT_URLS:
            return self.get_response(request)

        # Якщо не авторизований
        if not request.user.is_authenticated:
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")

        return self.get_response(request)



class RoleAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        try:
            resolver_match = resolve(request.path)
            view_name = resolver_match.view_name
        except Resolver404:
            return self.get_response(request)

        role = request.user.role

        # Адмін має доступ всюди
        if role == 'admin':
            return self.get_response(request)

        # Тільки адмін може на users
        if view_name == 'users':
            return redirect('welcome')

        # Гість
        if role == 'guest':
            if view_name == 'about_project' or view_name in EXEMPT_URLS:
                return self.get_response(request)
            return redirect('about_project')

        return self.get_response(request)