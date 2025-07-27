from django.contrib import admin
from accounts.models import FacilityForgeUser, Team


@admin.register(FacilityForgeUser)
class FacilityForgeUserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'phone_number',
        'is_staff',
        'is_active',
        'date_joined'
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('username',)
    ordering = ('username',)
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password', 'is_staff', 'is_active', 'groups', 'user_permissions')
        }),
        ('Personal Info', {
            'fields': ('first_name', 'last_name', 'phone_number')
        }),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'team_owner', 'manager')
    search_fields = ('name', 'team_owner__username', 'manager__username')
    list_filter = ('team_owner', 'manager')
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'team_owner', 'manager')
        }),
        ('Members', {
            'fields': ('members',)
        }),
    )