from django.shortcuts import render
from rest_framework import generics
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.serializers import ValidationError

# Create your views here.

class ListView(generics.ListAPIView):
    """
    Book List View
    
    Provides read-only access to list all books in the system.
    
    Configuration:
        - View Type: ListAPIView (handles GET requests for collections)
        - Queryset: Returns all Book objects from the database
        - Serializer: Uses BookSerializer to format response data
        - Permissions: ReadOnly - allows GET requests without authentication
    
    Intended Operation:
        - Accepts GET requests to retrieve a list of all books
        - Returns a JSON array of book objects
        - No authentication required (public read access)
        - Does not support POST, PUT, PATCH, or DELETE operations
    
    Custom Settings:
        - permission_classes: Set to [ReadOnly] to allow unauthenticated read access
          while preventing write operations
    
    URL Pattern: /api/books/
    HTTP Methods: GET
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class DetailView(generics.RetrieveAPIView):
    """
    Book Detail View
    
    Provides read-only access to retrieve a single book by its primary key.
    
    Configuration:
        - View Type: RetrieveAPIView (handles GET requests for single objects)
        - Queryset: Returns all Book objects (filtered by pk in URL)
        - Serializer: Uses BookSerializer to format response data
        - Permissions: ReadOnly - allows GET requests without authentication
    
    Intended Operation:
        - Accepts GET requests with a book ID in the URL
        - Returns a single book object as JSON
        - No authentication required (public read access)
        - Does not support POST, PUT, PATCH, or DELETE operations
    
    Custom Settings:
        - permission_classes: Set to [ReadOnly] to allow unauthenticated read access
          while preventing write operations
    
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