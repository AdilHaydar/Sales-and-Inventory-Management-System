from django.shortcuts import render
from django.views.generic import View, ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Customer
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.db.models import Sum, Case, When, F, DecimalField, Value
# Create your views here.


class CustomerListView(ListView):
    model = Customer
    template_name = 'customers/home.html'
    context_object_name = 'customers'
    
    def get_paginate_by(self, queryset):
        limit = self.request.GET.get('limit')
        try:
            return int(limit) if limit else 20
        except ValueError:
            return 20

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        return self.model.objects.filter(is_active=True, company_name__icontains=search_query).annotate(
            pending_total=Sum(
                Case(
                    When(orders__status='pending',
                        then=F('orders__quantity') * F('orders__price')),
                    default=Value(0),
                    output_field=DecimalField()
                )
            ),
            completed_total=Sum(
                Case(
                    When(orders__status='completed',
                        then=F('orders__quantity') * F('orders__price')),
                    default=Value(0),
                    output_field=DecimalField()
                )
            )
        ).order_by('company_name')
    


class CustomerCreateView(CreateView):
    model = Customer
    fields = ['company_name', 'contact_email', 'contact_phone', 'address']

    def get(self, request, *args, **kwargs):
        html = render_to_string('customers/partials/customer_create_partial.html', request=request)
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
        

class CustomerUpdateView(UpdateView):
    model = Customer
    fields = ['company_name', 'contact_email', 'contact_phone', 'address']
    http_method_names = ['post']

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

class CustomerDeleteView(DeleteView):
    model = Customer

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return JsonResponse({'success': True})
    
    def get(self, request, *args, **kwargs):
        return JsonResponse({'success': False, 'errors': 'Method not allowed'})

