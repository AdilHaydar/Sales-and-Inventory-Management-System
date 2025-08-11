
from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()

@register.filter
def json_script(customer, element_id):
    data = {
        'company_name': customer.company_name,
        'contact_email': customer.contact_email or '',
        'contact_phone': customer.contact_phone or '',
        'address': customer.address or '',
        'is_active': customer.is_active,
        'credit': "{:.2f}".format(customer.credit) or 0,
    }
    return mark_safe(json.dumps(data))

