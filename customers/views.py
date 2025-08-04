from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from .models import Customer
from products.models import Product
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.db.models import Sum, Case, When, F, DecimalField, Value
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F, ExpressionWrapper, DecimalField, Sum
from decimal import Decimal
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
    
class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'customers/detail.html'
    context_object_name = 'customer'

    def filters(self, params):
        filters = {}
        status = None
        exclude_status = params.pop("exclude_status", None)
        if exclude_status:
            status = params.pop("status", None)

        for key, value in params.items():
            if value:
                if key == 'start_date':
                    filters['order_date__date__gte'] = value
                elif key == 'end_date':
                    filters['order_date__date__lte'] = value
                elif key in ['product', 'status']:
                    filters[key] = value
        return (filters, (exclude_status, status))
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filters, (exclude_status, status) = self.filters(self.request.GET.copy())
        orders = context['object'].orders.filter(**filters)
        if exclude_status and status:
            orders = orders.exclude(status__in=status)
        context['orders'] = orders
        
        annotated_queryset = context['object'].orders.annotate(total_amount = ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField()))
        total_pending = annotated_queryset.filter(status='pending').aggregate(
            total_pending=Sum('total_amount'))["total_pending"] or 0
        
        total_cancelled = annotated_queryset.filter(status='cancelled').aggregate(
            total_cancelled=Sum('total_amount'))["total_cancelled"] or 0

        total_completed = annotated_queryset.filter(status='completed').aggregate(
            total_completed=Sum('total_amount'))["total_completed"] or 0
        
        total_amount = sum(order.total_price for order in orders)
        total_total = sum(order.total_price for order in annotated_queryset)
        
        context['total_pending'] = "{:.2f}".format(total_pending)
        context['total_completed'] = "{:.2f}".format(total_completed)
        context['total_cancelled'] = "{:.2f}".format(total_cancelled)
        context['total_amount'] = "{:.2f}".format(total_amount)
        context['total_total'] = "{:.2f}".format(total_total)

        context['products'] = Product.objects.values('id', 'name')
        
        return context


class CustomerCreateView(CreateView):
    model = Customer
    fields = ['company_name', 'contact_email', 'contact_phone', 'address']

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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

class CustomerDeleteView(DeleteView):
    model = Customer

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

