from django.shortcuts import redirect

class RedirectRootMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Eğer istek kök URL'e ("/") yapıldıysa ve user zaten /orders/ dışında bir yerde değilse
        if request.path == "/":
            return redirect("/orders/")
        return self.get_response(request)
