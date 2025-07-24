

from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth import authenticate
import base64

EXEMPT_URLS = [
    '/admin/login/',
    '/login/',
    '/signup/',
    '/static/',
    '/media/',
    '/admin',
]

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        if not request.user.is_authenticated:
            auth_header = request.META.get('HTTP_AUTHORIZATION')
            if auth_header and auth_header.startswith('Basic '):
                encoded_credentials = auth_header.split(' ')[1]
                decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
                username, password = decoded_credentials.split(':')
                user = authenticate(username=username, password=password)
                if user:
                    request.user = user

        if not request.user.is_authenticated and not any(path.startswith(url) for url in EXEMPT_URLS):
            return redirect(settings.LOGIN_URL)

        return self.get_response(request)
