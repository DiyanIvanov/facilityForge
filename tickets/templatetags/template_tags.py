from django import template
from django.template.defaultfilters import lower

register = template.Library()

@register.filter
def filter_by_priority(tickets, level):
    return tickets.filter(priority__iexact=level.lower())

@register.filter
def filter_by_facility(tickets, facility_id):
    return tickets.filter(facility_id=facility_id)
