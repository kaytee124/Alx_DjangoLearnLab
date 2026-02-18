# Advanced API Project

A Django REST Framework project demonstrating advanced API patterns with model relationships and nested serialization.

## Project Overview

This project implements a book management API with authors and books, showcasing how to handle one-to-many relationships in Django REST Framework using nested serializers.

## Models

### Author Model

The `Author` model represents authors in the system.

**Purpose:**
- Stores basic information about authors who have written books
- Serves as the parent model in a one-to-many relationship with books

**Fields:**
- `id`: Auto-generated primary key
- `name`: The full name of the author (CharField, max_length=100)

**Relationships:**
- Has a one-to-many relationship with the `Book` model
- One author can have many books
- The relationship is defined in the `Book` model via ForeignKey

**Example Usage:**
```python
author = Author.objects.create(name="J.K. Rowling")
```

### Book Model

The `Book` model represents books in the system.

**Purpose:**
- Stores information about books and their publication details
- Maintains a foreign key relationship to the Author model

**Fields:**
- `id`: Auto-generated primary key
- `title`: The title of the book (CharField, max_length=100)
- `publication_year`: The year the book was published (IntegerField)
- `author`: Foreign key reference to the Author model (ForeignKey)

**Relationships:**
- Many-to-one relationship with Author (many books can belong to one author)
- Uses `CASCADE` deletion: if an author is deleted, all their books are also deleted
- The ForeignKey creates a reverse relationship on Author, accessible via `author.book_set`

**Example Usage:**
```python
book = Book.objects.create(
    title="Harry Potter and the Philosopher's Stone",
    publication_year=1997,
    author=author_instance
)
```

## Serializers

### BookSerializer

**Purpose:**
- Serializes and deserializes Book model instances for API interactions
- Handles the conversion of Book objects to JSON format and vice versa
- Validates incoming book data during creation/updates

**Fields:**
- `id`: Auto-generated primary key
- `title`: The book's title
- `publication_year`: The year the book was published
- `author`: Foreign key to Author (represented as author ID in JSON)

**Usage:**
Used in API endpoints to serialize book data for GET, POST, PUT, PATCH requests.

**Example JSON:**
```json
{
    "id": 1,
    "title": "Harry Potter and the Philosopher's Stone",
    "publication_year": 1997,
    "author": 1
}
```

### AuthorSerializer

**Purpose:**
- Serializes and deserializes Author model instances for API interactions
- Includes nested book information, providing a complete view of an author and all their associated books
- Validates incoming author data during creation/updates

**Fields:**
- `id`: Auto-generated primary key
- `name`: The author's name
- `books`: Nested list of all books written by this author (read-only)

## Relationship Handling in Serializers

The relationship between Author and Book is handled through a **nested serializer approach**:

### 1. Nested Serialization

The `books` field in `AuthorSerializer` uses `BookSerializer` with `many=True` to serialize multiple related Book objects. This creates a nested structure in the JSON response where each author object contains a list of their books.

### 2. Read-Only Books Field

The `read_only=True` parameter on the `books` field ensures that:
- Books are included in GET responses (read operations)
- Books cannot be created or updated directly through the Author endpoint
- Book creation/updates must be done through the Book endpoint
- This prevents accidental data modification and maintains data integrity

### 3. Reverse Relationship Access

Django automatically creates a reverse relationship from Author to Book through the ForeignKey. The serializer accesses this via the `books` field name, which Django REST Framework automatically resolves from the Book model's ForeignKey relationship.

### Example JSON Response

When retrieving an author, the response includes nested book information:

```json
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
        {
            "id": 2,
            "title": "Harry Potter and the Chamber of Secrets",
            "publication_year": 1998,
            "author": 1
        }
    ]
}
```

### Benefits of This Approach

1. **Complete Data in One Request**: When fetching an author, you get all their books in a single API call, reducing the number of requests needed.

2. **Data Integrity**: The read-only nature of the nested books field prevents accidental modifications through the author endpoint.

3. **Clear Separation of Concerns**: Book creation/updates are handled through the Book endpoint, while author endpoints provide read access to related books.

4. **Flexible API Design**: Clients can choose to fetch authors with or without nested books, depending on their needs.

## Project Structure

```
advanced-api-project/
├── api/
│   ├── models.py          # Author and Book models
│   ├── serializers.py     # BookSerializer and AuthorSerializer
│   ├── views.py           # API views
│   └── urls.py            # URL routing
├── advanced-api-project/
│   └── settings.py        # Django settings
├── manage.py              # Django management script
└── README.md              # This file
```

## Getting Started

1. Install dependencies:
```bash
pip install django djangorestframework
```

2. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Create a superuser:
```bash
python manage.py createsuperuser
```

4. Run the development server:
```bash
python manage.py runserver
```

## API Endpoints

(Note: Endpoints should be configured in `api/views.py` and `api/urls.py`)

- `/api/authors/` - List and create authors
- `/api/authors/<id>/` - Retrieve, update, or delete a specific author
- `/api/books/` - List and create books
- `/api/books/<id>/` - Retrieve, update, or delete a specific book

## Notes

- The Author-Book relationship uses CASCADE deletion, so deleting an author will delete all associated books
- The nested `books` field in AuthorSerializer is read-only to maintain data integrity
- Book creation should be done through the Book endpoint, not through the Author endpoint
