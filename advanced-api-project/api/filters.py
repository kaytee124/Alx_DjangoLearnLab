"""
Filter configurations for API views.

This module defines FilterSet classes that enable advanced filtering
capabilities for the Book model using django-filters.
"""

import django_filters
from .models import Book, Author


class BookFilter(django_filters.FilterSet):
    """
    FilterSet for Book model.
    
    Provides comprehensive filtering options for book queries:
    - Filter by exact title match
    - Filter by publication year (exact, range, or comparison)
    - Filter by author ID
    - Filter by author name (case-insensitive partial match)
    
    Usage:
        The filter is automatically applied when DjangoFilterBackend
        is used in a view with filterset_class = BookFilter.
    
    Query Parameters:
        - title: Exact match on book title
        - publication_year: Exact match on publication year
        - publication_year__gte: Books published in or after this year
        - publication_year__lte: Books published in or before this year
        - author: Filter by author ID (exact match)
        - author__name: Filter by author name (case-insensitive contains)
    """
    
    # Exact match filtering
    title = django_filters.CharFilter(
        field_name='title',
        lookup_expr='iexact',  # Case-insensitive exact match
        help_text="Filter by exact book title (case-insensitive)"
    )
    
    # Publication year filtering with multiple lookup options
    publication_year = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='exact',
        help_text="Filter by exact publication year"
    )
    
    publication_year__gte = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='gte',
        help_text="Filter books published in or after this year"
    )
    
    publication_year__lte = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='lte',
        help_text="Filter books published in or before this year"
    )
    
    # Author filtering
    author = django_filters.NumberFilter(
        field_name='author',
        lookup_expr='exact',
        help_text="Filter by author ID"
    )
    
    # Filter by author name (case-insensitive contains)
    author__name = django_filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains',  # Case-insensitive contains
        help_text="Filter by author name (case-insensitive partial match)"
    )
    
    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author', 'author__name']
