
from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()

@register.filter
def json_script(order, element_id):
    data = {
        'product': str(order.product),
        'customer': str(order.customer),
        'quantity': order.quantity,
        'price': str(order.price),
        'total_price': str(order.total_price),
        'status': order.status,
    }
    return mark_safe(json.dumps(data))

