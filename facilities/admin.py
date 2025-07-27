from django.contrib import admin

from facilities.models import Facility


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'manager')
    search_fields = ('name', 'owner__username', 'manager__username')
    list_filter = ('owner', 'manager')
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'location', 'owner', 'manager')
        }),
        ('teams', {
            'fields': ('engineering_teams',)
        }),
        ('tenants', {
            'fields': ('tenants',)
        })
    )

