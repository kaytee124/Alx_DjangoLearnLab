# API Project - Authentication and Permission Documentation

## Overview

This Django REST Framework (DRF) API project implements token-based authentication and custom permission classes to secure API endpoints. This document explains how authentication and permissions are configured and how they work.

## Table of Contents

1. [Authentication Setup](#authentication-setup)
2. [Permission Configuration](#permission-configuration)
3. [Token Retrieval](#token-retrieval)
4. [API Endpoints](#api-endpoints)
5. [Usage Examples](#usage-examples)
6. [Security Best Practices](#security-best-practices)

---

## Authentication Setup

### Configuration in `settings.py`

The Django REST Framework authentication is configured in `api_project/settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

### Authentication Classes Explained

#### 1. **TokenAuthentication**
- **Purpose**: Allows clients to authenticate using a token in the HTTP header
- **How it works**: 
  - Client sends token in `Authorization` header: `Authorization: Token <token_value>`
  - DRF validates the token against the database
  - If valid, associates the request with the corresponding user
- **Use case**: Primary authentication method for API clients (mobile apps, frontend, etc.)

#### 2. **SessionAuthentication**
- **Purpose**: Fallback authentication using Django's session framework
- **How it works**: Uses browser cookies for authentication
- **Use case**: Useful for API browsing via web interface (DRF browsable API)

### Default Behavior

- **All API endpoints require authentication** by default (due to `DEFAULT_PERMISSION_CLASSES`)
- If no authentication is provided, API returns `401 Unauthorized`
- Authentication classes are tried in order until one succeeds

---

## Permission Configuration

### Default Permissions

The default permission class is set to `IsAuthenticated`, meaning:
- Users must be authenticated to access any endpoint
- This applies globally unless overridden in individual views

### Custom Permission: `IsAdminUser`

Located in `api/permissions.py`:

```python
class IsAdminUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_superuser
```

**How it works:**
- **Safe methods** (GET, HEAD, OPTIONS): All authenticated users can access
- **Unsafe methods** (POST, PUT, PATCH, DELETE): Only superusers can perform these actions
- **Purpose**: Allows read access to all authenticated users, but restricts write operations to admins

### View-Level Permissions

#### `BookList` View
```python
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```
- **Authentication**: Uses default (TokenAuthentication + SessionAuthentication)
- **Permissions**: Uses default (`IsAuthenticated`)
- **Access**: Any authenticated user can list books

#### `BookViewSet` View
```python
class BookViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```
- **Authentication**: Explicitly uses `TokenAuthentication` only
- **Permissions**: Requires both `IsAuthenticated` AND `IsAdminUser`
- **Access**: 
  - **GET/HEAD/OPTIONS**: Any authenticated user
  - **POST/PUT/PATCH/DELETE**: Only superusers

---

## Token Retrieval

### Endpoint

**URL**: `/api/api-token-auth/`  
**Method**: `POST`  
**Authentication**: Not required (public endpoint)

### Request Format

**Content-Type**: `application/json` or `application/x-www-form-urlencoded`

**JSON Body:**
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

**Form Data:**
```
username=your_username&password=your_password
```

### Response Format

**Success (200 OK):**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

**Failure (400 Bad Request):**
```json
{
    "non_field_errors": [
        "Unable to log in with provided credentials."
    ]
}
```

### How Tokens Work

1. **Token Creation**: When a user successfully authenticates via `/api/api-token-auth/`, DRF:
   - Validates username and password
   - Creates or retrieves a `Token` object for that user
   - Returns the token string

2. **Token Storage**: Tokens are stored in the `authtoken_token` table
   - One token per user
   - Creating a new token replaces the old one

3. **Token Usage**: Include the token in subsequent API requests:
   ```
   Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
   ```

---

## API Endpoints

### Available Endpoints

| Endpoint | Method | Authentication | Permission | Description |
|----------|--------|----------------|------------|-------------|
| `/api/api-token-auth/` | POST | None | None | Obtain authentication token |
| `/api/books/` | GET | Required | IsAuthenticated | List all books |
| `/api/books_all/` | GET | Required | IsAuthenticated | List all books (ViewSet) |
| `/api/books_all/` | POST | Required | IsAdminUser | Create new book (admin only) |
| `/api/books_all/{id}/` | GET | Required | IsAuthenticated | Retrieve book details |
| `/api/books_all/{id}/` | PUT/PATCH | Required | IsAdminUser | Update book (admin only) |
| `/api/books_all/{id}/` | DELETE | Required | IsAdminUser | Delete book (admin only) |

---

## Usage Examples

### 1. Obtaining a Token

**Using cURL:**
```bash
curl -X POST http://localhost:8000/api/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

**Using Python requests:**
```python
import requests

response = requests.post(
    'http://localhost:8000/api/api-token-auth/',
    json={'username': 'admin', 'password': 'admin123'}
)
token = response.json()['token']
print(f"Token: {token}")
```

**Using JavaScript (fetch):**
```javascript
fetch('http://localhost:8000/api/api-token-auth/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        username: 'admin',
        password: 'admin123'
    })
})
.then(response => response.json())
.then(data => {
    const token = data.token;
    console.log('Token:', token);
});
```

### 2. Making Authenticated Requests

**Using cURL:**
```bash
curl -X GET http://localhost:8000/api/books/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

**Using Python requests:**
```python
import requests

token = "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
headers = {'Authorization': f'Token {token}'}

# List books
response = requests.get('http://localhost:8000/api/books/', headers=headers)
books = response.json()
print(books)

# Create book (admin only)
book_data = {'title': 'New Book', 'author': 'Author Name'}
response = requests.post(
    'http://localhost:8000/api/books_all/',
    headers=headers,
    json=book_data
)
```

**Using JavaScript (fetch):**
```javascript
const token = '9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b';

fetch('http://localhost:8000/api/books/', {
    method: 'GET',
    headers: {
        'Authorization': `Token ${token}`
    }
})
.then(response => response.json())
.then(data => console.log(data));
```

### 3. Error Responses

**401 Unauthorized** (No token or invalid token):
```json
{
    "detail": "Authentication credentials were not provided."
}
```

**403 Forbidden** (Authenticated but insufficient permissions):
```json
{
    "detail": "You do not have permission to perform this action."
}
```

---

## Security Best Practices

### 1. Token Security
- **Never commit tokens to version control**
- **Use HTTPS in production** to prevent token interception
- **Rotate tokens periodically** (delete and recreate)
- **Store tokens securely** on the client side (not in localStorage for web apps)

### 2. Permission Design
- **Principle of Least Privilege**: Grant minimum permissions necessary
- **Separate read and write permissions**: Use custom permissions like `IsAdminUser`
- **Validate permissions at both view and object level**

### 3. Production Considerations
- **Set `DEBUG = False`** in production
- **Use environment variables** for sensitive settings
- **Implement rate limiting** to prevent abuse
- **Monitor authentication failures** for security threats
- **Use HTTPS only** (`SECURE_SSL_REDIRECT = True`)

### 4. Token Management
- **One token per user**: Creating a new token invalidates the old one
- **Token expiration**: Consider implementing token expiration for enhanced security
- **Token revocation**: Implement a mechanism to revoke tokens if compromised

---

## Code Structure

### Files Involved in Authentication

```
api_project/
├── api_project/
│   └── settings.py          # DRF authentication configuration
├── api/
│   ├── views.py            # View classes with authentication/permissions
│   ├── permissions.py      # Custom permission classes
│   ├── urls.py             # URL routing including token endpoint
│   └── models.py           # Data models
└── README.md               # This file
```

### Key Components

1. **settings.py**: Global DRF authentication and permission defaults
2. **views.py**: View-specific authentication and permission overrides
3. **permissions.py**: Custom permission logic
4. **urls.py**: Token retrieval endpoint routing

---

## Testing Authentication

### Test Token Retrieval
```bash
# Test token endpoint
curl -X POST http://localhost:8000/api/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'
```

### Test Protected Endpoint
```bash
# Without token (should fail)
curl http://localhost:8000/api/books/

# With token (should succeed)
curl -H "Authorization: Token YOUR_TOKEN_HERE" \
  http://localhost:8000/api/books/
```

### Test Admin-Only Endpoint
```bash
# As regular user (should fail for POST/PUT/DELETE)
curl -X POST \
  -H "Authorization: Token REGULAR_USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Book"}' \
  http://localhost:8000/api/books_all/

# As admin (should succeed)
curl -X POST \
  -H "Authorization: Token ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Book"}' \
  http://localhost:8000/api/books_all/
```

---

## Troubleshooting

### Common Issues

1. **"Authentication credentials were not provided"**
   - **Solution**: Include `Authorization: Token <token>` header in request

2. **"Invalid token"**
   - **Solution**: Token may have been regenerated. Obtain a new token

3. **"You do not have permission to perform this action"**
   - **Solution**: User lacks required permissions. Check if user is superuser for write operations

4. **Token endpoint returns 400**
   - **Solution**: Verify username and password are correct

---

## Additional Resources

- [Django REST Framework Authentication](https://www.django-rest-framework.org/api-guide/authentication/)
- [Django REST Framework Permissions](https://www.django-rest-framework.org/api-guide/permissions/)
- [Token Authentication Guide](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)

---

**Last Updated**: 2024  
**Project**: API Project with Token Authentication  
**Framework**: Django REST Framework
