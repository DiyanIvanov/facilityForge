from django.contrib import admin
from accounts.models import FacilityForgeUser


@admin.register(FacilityForgeUser)
class FacilityForgeUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('username',)
    ordering = ('username',)
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'phone_number')
        }),
    )
