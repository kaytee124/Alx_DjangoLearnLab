from django.contrib import admin

# Register your models here.
from .models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Fields displayed in the list view
    list_display = ('title', 'author', 'publication_year')

    # Sidebar filters
    list_filter = ('author', 'publication_year')

    # Search bar fields
    search_fields = ('title', 'author')
