from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'username', 'first_name', 'is_viewer', 'is_editor']
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('image', 'is_viewer', 'is_editor')
        })
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2', 'is_viewer', 'is_editor')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('image', 'is_viewer', 'is_editor')
        })
    )


class VehiclesAdmin(admin.ModelAdmin):
    list_display = ('v_number', 'v_manufacture', 'v_model',  'v_date_of_prod')


class GlassesAdmin(admin.ModelAdmin):
    list_display = ('g_damage_side', 'g_damage_type', 'g_model', 'g_source')
    list_display_links = ('g_model',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Vehicles, VehiclesAdmin)
admin.site.register(Glasses, GlassesAdmin)
