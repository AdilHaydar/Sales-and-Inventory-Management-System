from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from .models import Product
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = 'products/home.html'
    context_object_name = 'products'
    

    def get_paginate_by(self, queryset):
        limit = self.request.GET.get('limit')
        try:
            return int(limit) if limit else 20
        except ValueError:
            return 20

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        queryset = super().get_queryset().filter(is_active=True, name__icontains=search_query)
        return queryset

    def get_ordering(self):
        ordering = [
            self.request.GET.get('ordering_stock'),
            self.request.GET.get('ordering_price')
        ]
        return [field for field in ordering if field]

    

class ProductCreateView(CreateView):
    model = Product
    fields = ['name', 'description', 'price', 'stock']

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        html = render_to_string('products/partials/product_create_partial.html', {}, request=request)
        return HttpResponse(html)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.object = form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
        
class ProductUpdateView(UpdateView):
    model = Product
    fields = ['name', 'description', 'price', 'stock']
    http_method_names = ['post']

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            self.object = form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    
class ProductDeleteView(DeleteView):
    model = Product

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return JsonResponse({'success': True})
    
    def get(self, request, *args, **kwargs):
        return JsonResponse({'success': False, 'errors': 'Method not allowed'})