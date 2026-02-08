from django.contrib import admin

# Register your models here.
from .models import Book
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser



@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Fields displayed in the list view
    list_display = ('title', 'author', 'publication_year')

    # Sidebar filters
    list_filter = ('author', 'publication_year')

    # Search bar fields
    search_fields = ('title', 'author')





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

