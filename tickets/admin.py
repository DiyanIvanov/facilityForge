from django.contrib import admin
from tickets.models import Tickets, TicketMessages


@admin.register(Tickets)
class TicketsAdmin(admin.ModelAdmin):
    list_display = ('title', 'facility', 'status', 'created_at')
    search_fields = ('title', 'facility__name')
    list_filter = ('status', 'facility')
    ordering = ('-created_at',)


@admin.register(TicketMessages)
class TicketMessagesAdmin(admin.ModelAdmin):
    list_display = ('sender', 'ticket', 'ticket__facility', 'created_at',)
    search_fields = ('ticket__title', 'sender__username', 'ticket__facility__name', 'content')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


