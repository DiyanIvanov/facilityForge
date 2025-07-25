from django.contrib import admin
from tickets.models import Tickets


@admin.register(Tickets)
class TicketsAdmin(admin.ModelAdmin):
    list_display = ('title', 'facility', 'status', 'created_at')
    search_fields = ('title', 'facility__name')
    list_filter = ('status', 'facility')
    ordering = ('-created_at',)

