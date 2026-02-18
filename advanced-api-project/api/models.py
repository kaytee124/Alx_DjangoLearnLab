from django.db import models

# Create your models here.

class Author(models.Model):
    """
    Author Model
    
    Represents an author in the system. This model stores basic information
    about authors who have written books.
    
    Attributes:
        name (CharField): The full name of the author. Maximum length is 100 characters.
        
    Relationships:
        - Has a one-to-many relationship with Book model (one author can have many books)
        - This relationship is defined in the Book model via ForeignKey
        
    Example:
        author = Author.objects.create(name="J.K. Rowling")
    """
    name = models.CharField(max_length=100)
    
    def __str__(self):
        """String representation of the Author model."""
        return self.name


class Book(models.Model):
    """
    Book Model
    
    Represents a book in the system. Each book is associated with an author
    through a foreign key relationship.
    
    Attributes:
        title (CharField): The title of the book. Maximum length is 100 characters.
        publication_year (IntegerField): The year the book was published.
        author (ForeignKey): A foreign key reference to the Author model.
                           Uses CASCADE deletion, meaning if an author is deleted,
                           all their books will also be deleted.
    
    Relationships:
        - Many-to-one relationship with Author (many books can belong to one author)
        - The ForeignKey creates a reverse relationship on Author, accessible via
          author.book_set or author.books (if related_name is specified)
    
    Example:
        book = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone",
            publication_year=1997,
            author=author_instance
        )
    """
    title = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    def __str__(self):
        """String representation of the Book model."""
        return f"{self.title} by {self.author.name}"