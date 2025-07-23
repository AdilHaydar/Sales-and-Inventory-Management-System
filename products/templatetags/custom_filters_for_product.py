
from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()

@register.filter
def json_script(product, element_id):
    data = {
        'name': str(product.name),
        'quantity': str(product.stock),
        'price': str(product.price),
        'status': product.description,
    }
    return mark_safe(json.dumps(data))

