from rest_framework import serializers
from .models import Author, Book

class BookSerializer(serializers.ModelSerializer):
    """
    Book Serializer
    
    Serializes and deserializes Book model instances for API interactions.
    This serializer handles the conversion of Book objects to JSON format
    and vice versa.
    
    Purpose:
        - Validates incoming book data during creation/updates
        - Converts Book model instances to JSON for API responses
        - Handles the foreign key relationship with Author (author field)
    
    Fields:
        - id: Auto-generated primary key
        - title: The book's title
        - publication_year: The year the book was published
        - author: Foreign key to Author (represented as author ID in JSON)
    
    Usage:
        Used in API endpoints to serialize book data for GET, POST, PUT, PATCH requests.
    """
    class Meta:
        model = Book
        fields = '__all__'
    
    def validate_publication_year(self, value):
        if value < 1900:
            raise serializers.ValidationError("Publication year must be greater than 1900")
        return value
    
    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long")
        return value
    
    def validate_author(self, value):
        if value is None:
            raise serializers.ValidationError("Author is required")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    """
    Author Serializer
    
    Serializes and deserializes Author model instances for API interactions.
    This serializer includes nested book information, providing a complete
    view of an author and all their associated books.
    
    Purpose:
        - Validates incoming author data during creation/updates
        - Converts Author model instances to JSON for API responses
        - Includes nested book information using BookSerializer
    
    Fields:
        - id: Auto-generated primary key
        - name: The author's name
        - books: Nested list of all books written by this author (read-only)
    
    Relationship Handling:
        The relationship between Author and Book is handled through a nested
        serializer approach:
        
        1. **Nested Serialization**: The 'books' field uses BookSerializer with
           `many=True` to serialize multiple related Book objects. This creates
           a nested structure in the JSON response.
        
        2. **Read-Only Books**: The `read_only=True` parameter ensures that:
           - Books are included in GET responses (read operations)
           - Books cannot be created/updated directly through the Author endpoint
           - Book creation/updates must be done through the Book endpoint
        
        3. **Reverse Relationship**: Django automatically creates a reverse
           relationship from Author to Book through the ForeignKey. The serializer
           accesses this via the 'books' field name, which Django REST Framework
           automatically resolves from the Book model's ForeignKey.
        
        Example JSON Response:
        {
            "id": 1,
            "name": "J.K. Rowling",
            "books": [
                {
                    "id": 1,
                    "title": "Harry Potter and the Philosopher's Stone",
                    "publication_year": 1997,
                    "author": 1
                },
                ...
            ]
        }
    
    Usage:
        Used in API endpoints to serialize author data with nested book information
        for GET, POST, PUT, PATCH requests.
    """
    books = BookSerializer(many=True, read_only=True)
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
    
    def validate_name(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long")
        return value
