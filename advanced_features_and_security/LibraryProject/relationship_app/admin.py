from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class ModelAdmin(UserAdmin):
    model = CustomUser

    list_display = (
        'username',
        'email',
        'first_name',
        'last_name',
        'date_of_birth',
        'is_staff',
        'is_active',
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_picture'),
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_picture'),
        }),
    )


admin.site.register(CustomUser, ModelAdmin)

