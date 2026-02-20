from django.shortcuts import render
from rest_framework import generics
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.serializers import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter as DRFSearchFilter
from rest_framework.filters import OrderingFilter as DRFOrderingFilter

# Alias SearchFilter and OrderingFilter as filters.SearchFilter and filters.OrderingFilter for consistency
filters.SearchFilter = DRFSearchFilter
filters.OrderingFilter = DRFOrderingFilter

# Create your views here.

# FilterSet class defined inline in views.py (not in separate file)
class BookFilter(filters.FilterSet):
    """
    Book FilterSet
    
    Defines filtering options for the Book model. This FilterSet allows users
    to filter books by various attributes using different lookup expressions.
    
    Filter Fields:
        - title: Filter by book title (case-insensitive exact match)
        - title__icontains: Filter by book title (case-insensitive partial match)
        - publication_year: Filter by exact publication year
        - publication_year__gte: Filter books published in or after this year
        - publication_year__lte: Filter books published in or before this year
        - author: Filter by author ID (exact match)
        - author__name: Filter by author name (case-insensitive partial match)
        - author__name__iexact: Filter by author name (case-insensitive exact match)
    
    Usage Examples:
        - /api/books/?title=Harry Potter
        - /api/books/?publication_year=1997
        - /api/books/?publication_year__gte=2000
        - /api/books/?author__name=Rowling
        - /api/books/?title__icontains=potter&publication_year__gte=1997
    """
    title = filters.CharFilter(lookup_expr='iexact', help_text="Filter by exact book title (case-insensitive)")
    title__icontains = filters.CharFilter(field_name='title', lookup_expr='icontains', help_text="Filter by book title containing text (case-insensitive)")
    publication_year = filters.NumberFilter(lookup_expr='exact', help_text="Filter by exact publication year")
    publication_year__gte = filters.NumberFilter(field_name='publication_year', lookup_expr='gte', help_text="Filter books published in or after this year")
    publication_year__lte = filters.NumberFilter(field_name='publication_year', lookup_expr='lte', help_text="Filter books published in or before this year")
    author = filters.NumberFilter(lookup_expr='exact', help_text="Filter by author ID")
    author__name = filters.CharFilter(field_name='author__name', lookup_expr='icontains', help_text="Filter by author name containing text (case-insensitive)")
    author__name__iexact = filters.CharFilter(field_name='author__name', lookup_expr='iexact', help_text="Filter by exact author name (case-insensitive)")
    
    class Meta:
        model = Book
        fields = ['title', 'publication_year', 'author']


class ListView(generics.ListAPIView):
    """
    Book List View
    
    Provides read-only access to list all books in the system with advanced
    filtering, searching, and ordering capabilities.
    
    Configuration:
        - View Type: ListAPIView (handles GET requests for collections)
        - Queryset: Returns all Book objects from the database
        - Serializer: Uses BookSerializer to format response data
        - Permissions: IsAuthenticatedOrReadOnly - allows GET without authentication,
          requires authentication for write operations
    
    Intended Operation:
        - Accepts GET requests to retrieve a list of books
        - Supports filtering, searching, and ordering via query parameters
        - Returns a JSON array of book objects
        - Public read access (no authentication required for GET)
        - Does not support POST, PUT, PATCH, or DELETE operations
    
    Filtering Capabilities:
        Uses DjangoFilterBackend with BookFilter for advanced filtering:
        - title: Exact match on book title (case-insensitive)
        - title__icontains: Partial match on book title (case-insensitive)
        - publication_year: Exact match on publication year
        - publication_year__gte: Books published in or after this year
        - publication_year__lte: Books published in or before this year
        - author: Filter by author ID (exact match)
        - author__name: Filter by author name (case-insensitive partial match)
        - author__name__iexact: Filter by exact author name (case-insensitive)
        
        Example: /api/books/?publication_year=1997&author__name=Rowling
    
    Search Functionality:
        Uses SearchFilter to perform text searches across multiple fields:
        - title: Searches in book titles
        - author__name: Searches in author names
        
        Example: /api/books/?search=Harry
    
    Ordering Capabilities:
        Uses OrderingFilter to sort results by any field:
        - title: Sort by book title (ascending or descending)
        - publication_year: Sort by publication year
        - author__name: Sort by author name
        - id: Sort by book ID
        
        Use '-' prefix for descending order.
        Example: /api/books/?ordering=-publication_year,title
    
    Custom Settings:
        - permission_classes: IsAuthenticatedOrReadOnly for flexible access control
        - filter_backends: DjangoFilterBackend, SearchFilter, OrderingFilter
        - filterset_class: BookFilter for advanced filtering options
        - search_fields: ['title', 'author__name'] for text search
        - ordering_fields: ['title', 'publication_year', 'author__name', 'id']
        - ordering: Default ordering (by id ascending)
    
    URL Pattern: /api/books/
    HTTP Methods: GET
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Filter backends: enables filtering, searching, and ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Advanced filtering using FilterSet (defined inline above)
    filterset_class = BookFilter
    
    # Search fields: performs case-insensitive text search
    search_fields = ['title', 'author__name']
    
    # Ordering fields: allows sorting by these fields
    ordering_fields = ['title', 'publication_year', 'author__name', 'id']
    
    # Default ordering (if no ordering parameter is provided)
    ordering = ['id']

class DetailView(generics.RetrieveAPIView):
    """
    Book Detail View
    
    Provides read-only access to retrieve a single book by its primary key.
    
    Configuration:
        - View Type: RetrieveAPIView (handles GET requests for single objects)
        - Queryset: Returns all Book objects (filtered by pk in URL)
        - Serializer: Uses BookSerializer to format response data
        - Permissions: IsAuthenticatedOrReadOnly - allows GET without authentication,
          requires authentication for write operations
    
    Intended Operation:
        - Accepts GET requests with a book ID in the URL
        - Returns a single book object as JSON
        - Public read access (no authentication required for GET)
        - Does not support POST, PUT, PATCH, or DELETE operations
    
    Note:
        Filtering, searching, and ordering are not applicable to this view
        since it retrieves a single object by primary key. These features
        are only available on list views.
    
    Custom Settings:
        - permission_classes: IsAuthenticatedOrReadOnly for flexible access control
    
    URL Pattern: /api/books/<int:pk>/
    HTTP Methods: GET
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CreateView(generics.CreateAPIView):
    """
    Create Book View
    
    Provides authenticated access to create new book entries.
    
    Configuration:
        - View Type: CreateAPIView (handles POST requests for object creation)
        - Queryset: Book.objects.all() (used for validation)
        - Serializer: Uses BookSerializer to validate and save data
        - Authentication: TokenAuthentication - requires a valid token in request headers
        - Permissions: IsAuthenticated - user must be logged in
    
    Intended Operation:
        - Accepts POST requests with book data in JSON format
        - Validates the incoming data using BookSerializer
        - Creates a new book instance in the database
        - Returns the created book object with HTTP 201 status
    
    Custom Hooks and Settings:
        1. **perform_create()**: Custom hook that extends default behavior
           - Automatically sets the book's author to the authenticated user
           - This hook is called after validation but before saving
           - Note: This assumes request.user is an Author instance or compatible
        
        2. **create()**: Overrides the default create method to add custom validation
           - Performs additional validation check for 'title' field
           - Raises ValidationError if title is missing
           - This runs before perform_create() and serializer validation
           - Extends default behavior by adding explicit title requirement check
    
    Authentication Requirements:
        - Request must include: Authorization: Token <token_value>
        - Token must be valid and associated with an authenticated user
    
    URL Pattern: /api/books/create/
    HTTP Methods: POST
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Custom hook called during object creation.
        
        Extends default behavior by automatically setting the author field
        to the currently authenticated user. This ensures that books are
        always associated with the user who created them.
        
        This hook runs after serializer validation but before the object
        is saved to the database.
        """
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Overrides the default create method to add custom validation.
        
        Custom Behavior:
            - Checks if 'title' field is present in request data
            - Raises ValidationError if title is missing
            - This validation happens before serializer validation
        
        This extends the default create behavior by adding an explicit
        title requirement check at the view level.
        """
        if request.data.get('title') is None:
            raise ValidationError("Title is required")
        return super().create(request, *args, **kwargs)


class UpdateView(generics.UpdateAPIView):
    """
    Update Book View
    
    Provides authenticated access to update existing book entries.
    
    Configuration:
        - View Type: UpdateAPIView (handles PUT and PATCH requests)
        - Queryset: Book.objects.all() (filtered by pk in URL)
        - Serializer: Uses BookSerializer to validate and update data
        - Authentication: TokenAuthentication - requires a valid token in request headers
        - Permissions: IsAuthenticated - user must be logged in
    
    Intended Operation:
        - Accepts PUT (full update) and PATCH (partial update) requests
        - Updates an existing book instance identified by primary key
        - Validates the incoming data using BookSerializer
        - Returns the updated book object with HTTP 200 status
    
    Custom Hooks and Settings:
        1. **perform_update()**: Custom hook that extends default behavior
           - Automatically sets the book's author to the authenticated user
           - This hook is called after validation but before saving
           - Ensures the author field is always updated to the current user
           - Note: This assumes request.user is an Author instance or compatible
        
        2. **update()**: Overrides the default update method to add custom validation
           - Performs additional validation check for 'title' field
           - Raises ValidationError if title is missing
           - This runs before perform_update() and serializer validation
           - Extends default behavior by adding explicit title requirement check
    
    Authentication Requirements:
        - Request must include: Authorization: Token <token_value>
        - Token must be valid and associated with an authenticated user
    
    URL Pattern: /api/books/<int:pk>/update/
    HTTP Methods: PUT, PATCH
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        Custom hook called during object update.
        
        Extends default behavior by automatically setting the author field
        to the currently authenticated user. This ensures that books are
        always associated with the user who last updated them.
        
        This hook runs after serializer validation but before the object
        is saved to the database.
        """
        serializer.save(author=self.request.user)

    def update(self, request, *args, **kwargs):
        """
        Overrides the default update method to add custom validation.
        
        Custom Behavior:
            - Checks if 'title' field is present in request data
            - Raises ValidationError if title is missing
            - This validation happens before serializer validation
        
        This extends the default update behavior by adding an explicit
        title requirement check at the view level.
        """
        if request.data.get('title') is None:
            raise ValidationError("Title is required")
        return super().update(request, *args, **kwargs)


class DeleteView(generics.DestroyAPIView):
    """
    Delete Book View
    
    Provides authenticated access to delete book entries.
    
    Configuration:
        - View Type: DestroyAPIView (handles DELETE requests)
        - Queryset: Book.objects.all() (filtered by pk in URL)
        - Serializer: Uses BookSerializer (for response formatting if needed)
        - Permissions: IsAuthenticated - user must be logged in
        - Authentication: Uses default authentication (inherits from settings)
    
    Intended Operation:
        - Accepts DELETE requests for a book identified by primary key
        - Permanently removes the book instance from the database
        - Returns HTTP 204 No Content on successful deletion
        - Returns HTTP 404 if book doesn't exist
    
    Custom Settings:
        - permission_classes: Set to [IsAuthenticated] to require user authentication
          Note: This view does not explicitly set authentication_classes, so it will
          use the default authentication method configured in Django REST Framework
          settings (typically SessionAuthentication)
    
    Authentication Requirements:
        - User must be authenticated (via default authentication method)
        - For TokenAuthentication, request must include: Authorization: Token <token_value>
    
    URL Pattern: /api/books/<int:pk>/delete/
    HTTP Methods: DELETE
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]