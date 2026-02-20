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
pip install django djangorestframework django-filter
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

## View Configurations

The API uses Django REST Framework's generic class-based views to handle different HTTP operations. Each view is configured with specific permissions, authentication, and custom hooks to extend default behavior.

### Book List View (`ListView`)

**View Type:** `ListAPIView`  
**Purpose:** Provides read-only access to list all books with advanced filtering, searching, and ordering

**Configuration:**
- **Queryset:** `Book.objects.all()` - Returns all books from database
- **Serializer:** `BookSerializer` - Formats book data for JSON response
- **Permissions:** `IsAuthenticatedOrReadOnly` - Allows GET without authentication, requires auth for writes
- **Filter Backends:** `DjangoFilterBackend`, `SearchFilter`, `OrderingFilter`
- **FilterSet:** `BookFilter` - Advanced filtering configuration (defined inline in views.py)
- **Search Fields:** `['title', 'author__name']` - Text search across these fields
- **Ordering Fields:** `['title', 'publication_year', 'author__name', 'id']` - Sortable fields

**Intended Operation:**
- Handles GET requests to retrieve a list of books
- Supports filtering, searching, and ordering via query parameters
- Returns JSON array of book objects
- Public read access (no authentication required for GET)
- Read-only (no POST, PUT, PATCH, DELETE)

**Advanced Features:**
- **Filtering:** Filter by title, publication year, author ID, or author name
- **Searching:** Text search across book titles and author names
- **Ordering:** Sort results by any configured field (ascending or descending)

**URL:** `/api/books/`  
**HTTP Methods:** GET

See the [Filtering, Searching, and Ordering](#filtering-searching-and-ordering) section for detailed usage examples.

---

### Book Detail View (`book_detail`)

**View Type:** `RetrieveAPIView`  
**Purpose:** Provides read-only access to retrieve a single book

**Configuration:**
- **Queryset:** `Book.objects.all()` - Filtered by primary key from URL
- **Serializer:** `BookSerializer` - Formats single book data for JSON response
- **Permissions:** `ReadOnly` - Allows GET without authentication, blocks write operations

**Intended Operation:**
- Handles GET requests with book ID in URL
- Returns single book object as JSON
- Public access (no authentication required)
- Read-only (no POST, PUT, PATCH, DELETE)

**URL:** `/api/books/<int:pk>/`  
**HTTP Methods:** GET

---

### Create Book View (`create_book`)

**View Type:** `CreateAPIView`  
**Purpose:** Provides authenticated access to create new books

**Configuration:**
- **Queryset:** `Book.objects.all()` - Used for validation
- **Serializer:** `BookSerializer` - Validates and saves incoming data
- **Authentication:** `TokenAuthentication` - Requires valid token in request headers
- **Permissions:** `IsAuthenticated` - User must be logged in

**Intended Operation:**
- Handles POST requests with book data in JSON format
- Validates data using BookSerializer
- Creates new book instance in database
- Returns created book with HTTP 201 status

**Custom Hooks and Settings:**

1. **`perform_create()` Hook:**
   - Extends default behavior by automatically setting the book's author
   - Sets `author` field to the authenticated user (`self.request.user`)
   - Called after validation but before saving to database
   - Ensures books are always associated with the user who created them

2. **`create()` Method Override:**
   - Adds custom validation at view level
   - Checks if 'title' field is present in request data
   - Raises `ValidationError` if title is missing
   - Runs before serializer validation and `perform_create()`

**Authentication Requirements:**
- Request header: `Authorization: Token <token_value>`
- Token must be valid and associated with authenticated user

**URL:** `/api/books/create/`  
**HTTP Methods:** POST

---

### Update Book View (`update_book`)

**View Type:** `UpdateAPIView`  
**Purpose:** Provides authenticated access to update existing books

**Configuration:**
- **Queryset:** `Book.objects.all()` - Filtered by primary key from URL
- **Serializer:** `BookSerializer` - Validates and updates data
- **Authentication:** `TokenAuthentication` - Requires valid token in request headers
- **Permissions:** `IsAuthenticated` - User must be logged in

**Intended Operation:**
- Handles PUT (full update) and PATCH (partial update) requests
- Updates existing book identified by primary key
- Validates data using BookSerializer
- Returns updated book with HTTP 200 status

**Custom Hooks and Settings:**

1. **`perform_update()` Hook:**
   - Extends default behavior by automatically updating the book's author
   - Sets `author` field to the authenticated user (`self.request.user`)
   - Called after validation but before saving to database
   - Ensures books are always associated with the user who last updated them

2. **`update()` Method Override:**
   - Adds custom validation at view level
   - Checks if 'title' field is present in request data
   - Raises `ValidationError` if title is missing
   - Runs before serializer validation and `perform_update()`

**Authentication Requirements:**
- Request header: `Authorization: Token <token_value>`
- Token must be valid and associated with authenticated user

**URL:** `/api/books/<int:pk>/update/`  
**HTTP Methods:** PUT, PATCH

---

### Delete Book View (`delete_book`)

**View Type:** `DestroyAPIView`  
**Purpose:** Provides authenticated access to delete books

**Configuration:**
- **Queryset:** `Book.objects.all()` - Filtered by primary key from URL
- **Serializer:** `BookSerializer` - Used for response formatting if needed
- **Permissions:** `IsAuthenticated` - User must be logged in
- **Authentication:** Uses default authentication (from DRF settings)

**Intended Operation:**
- Handles DELETE requests for book identified by primary key
- Permanently removes book instance from database
- Returns HTTP 204 No Content on success
- Returns HTTP 404 if book doesn't exist

**Custom Settings:**
- Only requires authentication (no custom hooks)
- Uses default authentication method from Django REST Framework settings

**Authentication Requirements:**
- User must be authenticated via default method
- For TokenAuthentication: `Authorization: Token <token_value>`

**URL:** `/api/books/<int:pk>/delete/`  
**HTTP Methods:** DELETE

---

## Custom Hooks and Behavior Extensions

### Understanding Custom Hooks

The views use Django REST Framework's hook system to extend default behavior:

1. **`perform_create()` / `perform_update()`:**
   - Called after serializer validation but before database save
   - Allows modification of data before saving
   - Used to automatically set author field to authenticated user
   - Can access `self.request` and `self.request.user`

2. **Method Overrides (`create()`, `update()`):**
   - Override entire request handling flow
   - Allow custom validation before serializer processing
   - Must call `super()` to maintain default behavior
   - Used to add explicit title validation

### Permission Classes

- **`ReadOnly`:** Allows GET requests without authentication, blocks all write operations
- **`IsAuthenticated`:** Requires user to be logged in for any operation

### Authentication Classes

- **`TokenAuthentication`:** Requires token in `Authorization` header
  - Format: `Authorization: Token <your-token-here>`
  - Tokens are generated for authenticated users
  - Provides stateless authentication

## Filtering, Searching, and Ordering

The Book List API (`GET /api/books/`) supports advanced query capabilities to help users efficiently access and manipulate data. These features are implemented using Django REST Framework's filter backends and django-filters.

### Implementation Overview

The filtering, searching, and ordering functionality is implemented in the `ListView` class in `api/views.py`:

1. **Filter Backends:** Three filter backends are configured:
   - `DjangoFilterBackend` - For field-based filtering
   - `SearchFilter` - For text search across multiple fields
   - `OrderingFilter` - For sorting results

2. **FilterSet Class:** A custom `BookFilter` class (defined inline in `views.py`) provides advanced filtering options with multiple lookup expressions.

3. **Search Fields:** Text search is enabled on `title` and `author__name` fields.

4. **Ordering Fields:** Results can be sorted by `title`, `publication_year`, `author__name`, or `id`.

### Filtering

Filtering allows you to narrow down results based on specific field values. The API supports filtering by:

#### Available Filter Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `title` | string | Exact match on book title (case-insensitive) | `?title=Harry Potter` |
| `title__icontains` | string | Book title containing text (case-insensitive) | `?title__icontains=potter` |
| `publication_year` | integer | Exact match on publication year | `?publication_year=1997` |
| `publication_year__gte` | integer | Books published in or after this year | `?publication_year__gte=2000` |
| `publication_year__lte` | integer | Books published in or before this year | `?publication_year__lte=1999` |
| `author` | integer | Filter by author ID (exact match) | `?author=1` |
| `author__name` | string | Filter by author name containing text (case-insensitive) | `?author__name=Rowling` |
| `author__name__iexact` | string | Exact match on author name (case-insensitive) | `?author__name__iexact=J.K. Rowling` |

#### Filtering Examples

**Filter by exact publication year:**
```bash
GET /api/books/?publication_year=1997
```

**Filter by author name (partial match):**
```bash
GET /api/books/?author__name=Rowling
```

**Filter books published after a certain year:**
```bash
GET /api/books/?publication_year__gte=2000
```

**Filter books published before a certain year:**
```bash
GET /api/books/?publication_year__lte=1999
```

**Filter by title containing text:**
```bash
GET /api/books/?title__icontains=potter
```

**Combine multiple filters:**
```bash
GET /api/books/?publication_year=1997&author__name=Rowling
```

**Filter by author ID:**
```bash
GET /api/books/?author=1
```

### Searching

Searching performs case-insensitive text search across multiple fields simultaneously. The search looks for the search term in:

- **Book titles** (`title` field)
- **Author names** (`author__name` field)

#### Search Parameter

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `search` | string | Text to search for in title and author name | `?search=Harry` |

#### Search Examples

**Search for books with "Harry" in title or author name:**
```bash
GET /api/books/?search=Harry
```

**Search for books by author name:**
```bash
GET /api/books/?search=Rowling
```

**Combine search with filtering:**
```bash
GET /api/books/?search=Potter&publication_year__gte=1997
```

**Note:** The search is case-insensitive and performs a "contains" match, so searching for "harry" will find "Harry Potter" books.

### Ordering

Ordering allows you to sort the results by one or more fields in ascending or descending order.

#### Ordering Parameter

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `ordering` | string | Comma-separated list of fields to sort by. Use `-` prefix for descending order | `?ordering=-publication_year` |

#### Available Ordering Fields

- `title` - Sort by book title
- `publication_year` - Sort by publication year
- `author__name` - Sort by author name
- `id` - Sort by book ID

#### Ordering Examples

**Sort by publication year (newest first):**
```bash
GET /api/books/?ordering=-publication_year
```

**Sort by publication year (oldest first):**
```bash
GET /api/books/?ordering=publication_year
```

**Sort by title (alphabetical):**
```bash
GET /api/books/?ordering=title
```

**Sort by title (reverse alphabetical):**
```bash
GET /api/books/?ordering=-title
```

**Multiple field sorting (year first, then title):**
```bash
GET /api/books/?ordering=-publication_year,title
```

**Sort by author name:**
```bash
GET /api/books/?ordering=author__name
```

### Combining Filtering, Searching, and Ordering

You can combine all three features in a single request:

```bash
GET /api/books/?publication_year__gte=1997&search=Potter&ordering=-publication_year,title
```

This request will:
1. Filter books published in 1997 or later
2. Search for "Potter" in titles and author names
3. Sort by publication year (newest first), then by title (alphabetical)

### Implementation Details

#### FilterSet Configuration

The `BookFilter` class in `api/views.py` defines the filtering capabilities:

```python
class BookFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='iexact')
    title__icontains = filters.CharFilter(field_name='title', lookup_expr='icontains')
    publication_year = filters.NumberFilter(lookup_expr='exact')
    publication_year__gte = filters.NumberFilter(field_name='publication_year', lookup_expr='gte')
    publication_year__lte = filters.NumberFilter(field_name='publication_year', lookup_expr='lte')
    author = filters.NumberFilter(lookup_expr='exact')
    author__name = filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    author__name__iexact = filters.CharFilter(field_name='author__name', lookup_expr='iexact')
```

#### View Configuration

The `ListView` class is configured with:

```python
filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
filterset_class = BookFilter
search_fields = ['title', 'author__name']
ordering_fields = ['title', 'publication_year', 'author__name', 'id']
ordering = ['id']  # Default ordering
```

### Testing the Features

You can test these features using:

1. **Browser:** Simply append query parameters to the URL
   ```
   http://localhost:8000/api/books/?search=Harry&ordering=-publication_year
   ```

2. **curl:**
   ```bash
   curl "http://localhost:8000/api/books/?publication_year=1997&ordering=title"
   ```

3. **Postman:**
   - Set request method to GET
   - Enter URL: `http://localhost:8000/api/books/`
   - Add query parameters in the Params tab

4. **Python requests:**
   ```python
   import requests
   
   response = requests.get(
       'http://localhost:8000/api/books/',
       params={
           'publication_year__gte': 2000,
           'search': 'Potter',
           'ordering': '-publication_year'
       }
   )
   ```

## API Endpoints

All endpoints are configured in `api/views.py` and `api/urls.py`:

**Book Endpoints:**
- `GET /api/books/` - List all books with filtering, searching, and ordering (public, read-only)
- `GET /api/books/<id>/` - Get single book (public, read-only)
- `POST /api/books/create/` - Create new book (authenticated, requires token)
- `PUT/PATCH /api/books/<id>/update/` - Update book (authenticated, requires token)
- `DELETE /api/books/<id>/delete/` - Delete book (authenticated)

**Query Parameters for List Endpoint:**
- Filtering: `title`, `title__icontains`, `publication_year`, `publication_year__gte`, `publication_year__lte`, `author`, `author__name`, `author__name__iexact`
- Searching: `search`
- Ordering: `ordering` (use `-` prefix for descending order)

## Notes

- The Author-Book relationship uses CASCADE deletion, so deleting an author will delete all associated books
- The nested `books` field in AuthorSerializer is read-only to maintain data integrity
- Book creation should be done through the Book endpoint, not through the Author endpoint
- All filtering, searching, and ordering logic is implemented inline in `api/views.py` (no separate filters file)
- The `BookFilter` FilterSet class is defined directly in `views.py` for simplicity and maintainability