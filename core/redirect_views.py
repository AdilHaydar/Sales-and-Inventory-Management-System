from django.shortcuts import redirect


def redirect_view_from_home(request):
    return redirect("orders:order_list", permanent=True)