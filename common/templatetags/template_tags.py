from django import template


register = template.Library()

@register.filter
def filter_by_priority(tickets, level):
    return tickets.filter(priority=level)

@register.filter
def filter_by_facility(tickets, facility_id):
    return tickets.filter(facility_id=facility_id)
