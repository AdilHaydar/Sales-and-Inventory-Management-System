from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Order, STATUS_CHOICES
from django.http import JsonResponse, HttpResponse
from django.db import transaction
from products.models import Product
from customers.models import Customer
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from weasyprint import HTML
from django.db.models import F, ExpressionWrapper, DecimalField, Sum
from datetime import datetime
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from decimal import Decimal, ROUND_DOWN



class OrderListView(ListView):
    template_name = 'orders/home.html'

    def get_paginate_by(self, queryset=None):
        limit = self.request.GET.get('limit')
        try:
            return int(limit) if limit else 20
        except ValueError:
            return 20

    def get(self, request):
        queryset = Order.objects.filter(customer__is_active=True)
        queryset_on_annotate = queryset.annotate(
            total_amount=ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField())
        )
        total_pending = queryset_on_annotate.filter(status='pending').aggregate(
            total_pending=Sum('total_amount'))['total_pending'] or 0

        total_completed = queryset_on_annotate.filter(status='completed').aggregate(
            total_completed=Sum('total_amount'))['total_completed'] or 0
        filters = {}
        params = request.GET.copy()

        for key, value in params.items():
            if value:
                if key == 'start_date':
                    filters['order_date__date__gte'] = value
                elif key == 'end_date':
                    filters['order_date__date__lte'] = value
                elif key in ['product', 'customer', 'status']:
                    filters[key] = value

        queryset = queryset.filter(**filters).annotate(
            total_amount=ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField())
        ).order_by('-order_date')

        

        paginate_by = self.get_paginate_by(queryset)
        paginator = Paginator(queryset, paginate_by)

        page_number = self.request.GET.get("page")
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        total_amount = sum(order.total_amount for order in page_obj)

        context = {
            'orders': page_obj,
            'customers': Customer.objects.filter(is_active=True),
            'products': Product.objects.all(),
            'statuses': STATUS_CHOICES,
            'total_amount': Decimal(total_amount).quantize(Decimal('0.00')),
            'total_pending': "{:.2f}".format(total_pending),
            'total_completed': "{:.2f}".format(total_completed),
            'is_paginated': page_obj.has_other_pages(),
        }

        return render(request, self.template_name, context)

    
class OrderCreateView(CreateView):
    model = Order
    fields = ['customer', 'product', 'quantity', 'price', 'status']

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(stock__gt=0, is_active=True)
        customers = Customer.objects.filter(is_active=True)
        html = render_to_string('orders/partials/new_order_form.html', {
            'products': products,
            'customers': customers,
        }, request=request)
        return HttpResponse(html)

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            try:
                with transaction.atomic():
                    product = Product.objects.select_for_update().get(pk=form.cleaned_data['product'].pk)

                    if form.cleaned_data['status'] == 'completed':
                        product.stock -=  form.cleaned_data['quantity']
                        product.save()

                    form.save() 
                return JsonResponse({'success': True})

            except (ValueError, ValidationError) as e:
                return JsonResponse({'success': False, 'errors': str(e)})

        return JsonResponse({'success': False, 'errors': form.errors})
        
       


class OrderUpdateView(UpdateView):
    model = Order
    fields = ['quantity', 'status', 'price']
    http_method_names = ['post']

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            try:
                with transaction.atomic():
                    product = Product.objects.select_for_update().get(pk=self.object.product.pk)
                    order = Order.objects.get(pk=self.object.pk)

                    if form.cleaned_data['status'] == 'completed':
                        if order.status != 'completed':
                            product.stock -= form.cleaned_data['quantity']
                        else:
                            product.stock += order.quantity - form.cleaned_data['quantity']
                        product.save()

                    form.save() 
                return JsonResponse({'success': True})

            except (ValidationError, ValueError) as e:
                return JsonResponse({'success': False, 'errors': str(e)}, status=400)

        return JsonResponse({'success': False, 'errors': form.errors}, status=400)


class OrderDeleteView(DeleteView):
    model = Order

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        product = Product.objects.select_for_update().get(pk=self.object.product.pk)
        
        if self.object.status == 'completed':
            product.stock += self.object.quantity
            product.save()

        self.object.delete()
        
        return JsonResponse({'success': True})


class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = self.object
        return context
    

class OrderPdfView(ListView):
    model = Order


    def get_paginate_by(self, queryset=None):
        limit = self.request.GET.get('limit')
        try:
            return int(limit) if limit else 20
        except ValueError:
            return 20

    def get(self, request, *args, **kwargs):
        queryset = Order.objects.filter(customer__is_active=True)
        filters = {}
        params = self.request.GET.copy()
        params.pop('limit', None)
        params.pop('page', None)

        for key, value in params.items():
            if value:
                if key == 'start_date':
                    filters['order_date__date__gte'] = value
                elif key == 'end_date':
                    filters['order_date__date__lte'] = value
                else:
                    filters[key] = value

        orders = queryset.filter(**filters).annotate(
            total_amount=ExpressionWrapper(F('price') * F('quantity'), output_field=DecimalField())
        ).order_by('-order_date')

        paginate_by = self.get_paginate_by(orders)
        paginator = Paginator(orders, paginate_by)

        page_number = self.request.GET.get("page")
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        total_amount = sum(order.total_amount for order in page_obj)

        html_string = render_to_string('orders/order_pdf.html', {
            'orders': page_obj,
            'total_amount': total_amount,
            'now': datetime.now(),
        })

        html = HTML(string=html_string)
        pdf = html.write_pdf()

        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="orders.pdf"'
        return response