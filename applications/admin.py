from django.contrib import admin
from applications.models import Applications


@admin.register(Applications)
class ApplicationsAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'status', 'created')
    search_fields = ('applicant__username', 'applicant__first_name', 'applicant__last_name')
    list_filter = ('status', 'applicant')
    ordering = ('-created',)
    fieldsets = (
        (None, {
            'fields': ('applicant', 'description', 'status', 'created')
        }),
        ('Details', {
            'fields': ('team','facility',)
        }),
    )
    readonly_fields = ('created',)
