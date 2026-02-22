# Social Media API

A Django REST Framework API for a social media platform with user accounts, posts, and comments functionality.

## Table of Contents

- [Authentication](#authentication)
- [User Management API](#user-management-api)
- [Posts API](#posts-api)
- [Comments API](#comments-api)
- [Feed API](#feed-api)
- [Models](#models)
- [Error Handling](#error-handling)

## Base URL

```
http://localhost:8000/api/
```

## Authentication

All endpoints (except registration and login) require authentication using Token Authentication. Include the token in the request headers:

```
Authorization: Token <your_token_here>
```

### Register User

Create a new user account.

**Endpoint:** `POST /api/accounts/register/`

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response:** `201 Created`
```json
{
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "bio": "",
    "profile_picture": null
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

### Login

Authenticate and receive an authentication token.

**Endpoint:** `POST /api/accounts/login/`

**Request Body:**
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```

**Response:** `200 OK`
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "bio": "",
    "profile_picture": null
  }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepassword123"
  }'
```

---

## User Management API

The user management endpoints allow authenticated users to follow and unfollow other users. Users can only modify their own following list.

### Follow a User

Follow another user to see their posts in your feed.

**Endpoint:** `POST /api/accounts/follow/<int:user_id>/`

**Headers:**
```
Authorization: Token <your_token_here>
```

**Response:** `200 OK`
```json
{
  "message": "You are now following janedoe",
  "user": {
    "id": 2,
    "username": "janedoe",
    "email": "jane@example.com",
    "bio": "Designer",
    "profile_picture": null
  }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/accounts/follow/2/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

**Error Responses:**

**400 Bad Request** - Already following:
```json
{
  "error": "You are already following this user."
}
```

**400 Bad Request** - Cannot follow yourself:
```json
{
  "error": "You cannot follow yourself."
}
```

**404 Not Found** - User doesn't exist:
```json
{
  "detail": "Not found."
}
```

### Unfollow a User

Unfollow a user to stop seeing their posts in your feed.

**Endpoint:** `POST /api/accounts/unfollow/<int:user_id>/`

**Headers:**
```
Authorization: Token <your_token_here>
```

**Response:** `200 OK`
```json
{
  "message": "You have unfollowed janedoe",
  "user": {
    "id": 2,
    "username": "janedoe",
    "email": "jane@example.com",
    "bio": "Designer",
    "profile_picture": null
  }
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/accounts/unfollow/2/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

**Error Responses:**

**400 Bad Request** - Not following:
```json
{
  "error": "You are not following this user."
}
```

**404 Not Found** - User doesn't exist:
```json
{
  "detail": "Not found."
}
```

**Notes:**
- Users can only modify their own following list (enforced by authentication)
- Users cannot follow themselves
- Following a user allows you to see their posts in your personalized feed
- Use `user.following.all()` to get all users you follow
- Use `user.followers.all()` to get all users who follow you

---

## Posts API

All post endpoints require authentication. Users can view all posts but can only edit or delete their own posts.

### List All Posts

Retrieve a list of all posts, ordered by creation date (newest first).

**Endpoint:** `GET /api/posts/`

**Headers:**
```
Authorization: Token <your_token_here>
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "author": {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "bio": "Software developer",
      "profile_picture": null
    },
    "title": "My First Post",
    "content": "This is the content of my first post!",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-15T10:30:00Z"
  },
  {
    "id": 2,
    "author": {
      "id": 2,
      "username": "janedoe",
      "email": "jane@example.com",
      "bio": "Designer",
      "profile_picture": null
    },
    "title": "Another Post",
    "content": "This is another post from a different user.",
    "created_at": "2024-01-15T09:15:00Z",
    "updated_at": "2024-01-15T09:15:00Z"
  }
]
```

**cURL Example:**
```bash
curl -X GET http://localhost:8000/api/posts/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

### Create a Post

Create a new post. The author is automatically set to the authenticated user.

**Endpoint:** `POST /api/posts/`

**Headers:**
```
Authorization: Token <your_token_here>
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "My New Post",
  "content": "This is the content of my new post. It can be as long as needed."
}
```

**Response:** `201 Created`
```json
{
  "id": 3,
  "author": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "bio": "Software developer",
    "profile_picture": null
  },
  "title": "My New Post",
  "content": "This is the content of my new post. It can be as long as needed.",
  "created_at": "2024-01-15T11:00:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My New Post",
    "content": "This is the content of my new post."
  }'
```

**Validation Rules:**
- `title`: Required, cannot be empty, maximum 200 characters
- `content`: Required, cannot be empty

### Retrieve a Specific Post

Get details of a specific post by ID.

**Endpoint:** `GET /api/posts/{id}/`

**Headers:**
```
Authorization: Token <your_token_here>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "author": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "bio": "Software developer",
    "profile_picture": null
  },
  "title": "My First Post",
  "content": "This is the content of my first post!",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

**cURL Example:**
```bash
curl -X GET http://localhost:8000/api/posts/1/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

### Update a Post

Update an existing post. Only the post author can update their own posts.

**Endpoint:** `PUT /api/posts/{id}/` or `PATCH /api/posts/{id}/`

**Headers:**
```
Authorization: Token <your_token_here>
Content-Type: application/json
```

**Request Body (PUT - full update):**
```json
{
  "title": "Updated Post Title",
  "content": "This is the updated content of my post."
}
```

**Request Body (PATCH - partial update):**
```json
{
  "title": "Updated Post Title"
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "author": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "bio": "Software developer",
    "profile_picture": null
  },
  "title": "Updated Post Title",
  "content": "This is the updated content of my post.",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T12:00:00Z"
}
```

**cURL Example (PUT):**
```bash
curl -X PUT http://localhost:8000/api/posts/1/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Post Title",
    "content": "This is the updated content."
  }'
```

**cURL Example (PATCH):**
```bash
curl -X PATCH http://localhost:8000/api/posts/1/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Post Title"
  }'
```

**Error Response (Not Owner):** `403 Forbidden`
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### Delete a Post

Delete a post. Only the post author can delete their own posts.

**Endpoint:** `DELETE /api/posts/{id}/`

**Headers:**
```
Authorization: Token <your_token_here>
```

**Response:** `204 No Content` (empty response body)

**cURL Example:**
```bash
curl -X DELETE http://localhost:8000/api/posts/1/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

**Error Response (Not Owner):** `403 Forbidden`
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## Comments API

All comment endpoints require authentication. Users can view all comments but can only edit or delete their own comments.

### List All Comments

Retrieve a list of all comments, ordered by creation date (newest first).

**Endpoint:** `GET /api/comments/`

**Headers:**
```
Authorization: Token <your_token_here>
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "post": 1,
    "author": {
      "id": 2,
      "username": "janedoe",
      "email": "jane@example.com",
      "bio": "Designer",
      "profile_picture": null
    },
    "content": "Great post! I really enjoyed reading this.",
    "created_at": "2024-01-15T11:00:00Z",
    "updated_at": "2024-01-15T11:00:00Z"
  },
  {
    "id": 2,
    "post": 1,
    "author": {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "bio": "Software developer",
      "profile_picture": null
    },
    "content": "Thanks for the feedback!",
    "created_at": "2024-01-15T11:15:00Z",
    "updated_at": "2024-01-15T11:15:00Z"
  }
]
```

**cURL Example:**
```bash
curl -X GET http://localhost:8000/api/comments/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

### Create a Comment

Create a new comment on a post. The author is automatically set to the authenticated user.

**Endpoint:** `POST /api/comments/`

**Headers:**
```
Authorization: Token <your_token_here>
Content-Type: application/json
```

**Request Body:**
```json
{
  "post": 1,
  "content": "This is my comment on the post."
}
```

**Response:** `201 Created`
```json
{
  "id": 3,
  "post": 1,
  "author": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "bio": "Software developer",
    "profile_picture": null
  },
  "content": "This is my comment on the post.",
  "created_at": "2024-01-15T12:00:00Z",
  "updated_at": "2024-01-15T12:00:00Z"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:8000/api/comments/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "post": 1,
    "content": "This is my comment on the post."
  }'
```

**Validation Rules:**
- `post`: Required, must be a valid post ID
- `content`: Required, cannot be empty

### Retrieve a Specific Comment

Get details of a specific comment by ID.

**Endpoint:** `GET /api/comments/{id}/`

**Headers:**
```
Authorization: Token <your_token_here>
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "post": 1,
  "author": {
    "id": 2,
    "username": "janedoe",
    "email": "jane@example.com",
    "bio": "Designer",
    "profile_picture": null
  },
  "content": "Great post! I really enjoyed reading this.",
  "created_at": "2024-01-15T11:00:00Z",
  "updated_at": "2024-01-15T11:00:00Z"
}
```

**cURL Example:**
```bash
curl -X GET http://localhost:8000/api/comments/1/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

### Update a Comment

Update an existing comment. Only the comment author can update their own comments.

**Endpoint:** `PUT /api/comments/{id}/` or `PATCH /api/comments/{id}/`

**Headers:**
```
Authorization: Token <your_token_here>
Content-Type: application/json
```

**Request Body (PUT - full update):**
```json
{
  "post": 1,
  "content": "This is my updated comment."
}
```

**Request Body (PATCH - partial update):**
```json
{
  "content": "This is my updated comment."
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "post": 1,
  "author": {
    "id": 2,
    "username": "janedoe",
    "email": "jane@example.com",
    "bio": "Designer",
    "profile_picture": null
  },
  "content": "This is my updated comment.",
  "created_at": "2024-01-15T11:00:00Z",
  "updated_at": "2024-01-15T12:30:00Z"
}
```

**cURL Example (PUT):**
```bash
curl -X PUT http://localhost:8000/api/comments/1/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "post": 1,
    "content": "This is my updated comment."
  }'
```

**cURL Example (PATCH):**
```bash
curl -X PATCH http://localhost:8000/api/comments/1/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "This is my updated comment."
  }'
```

**Error Response (Not Owner):** `403 Forbidden`
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### Delete a Comment

Delete a comment. Only the comment author can delete their own comments.

**Endpoint:** `DELETE /api/comments/{id}/`

**Headers:**
```
Authorization: Token <your_token_here>
```

**Response:** `204 No Content` (empty response body)

**cURL Example:**
```bash
curl -X DELETE http://localhost:8000/api/comments/1/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

**Error Response (Not Owner):** `403 Forbidden`
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## Feed API

The feed endpoint provides a personalized view of posts from users that the authenticated user follows.

### Get Personalized Feed

Retrieve posts from users you follow, ordered by creation date (newest first).

**Endpoint:** `GET /api/feed/`

**Headers:**
```
Authorization: Token <your_token_here>
```

**Response:** `200 OK`
```json
[
  {
    "id": 5,
    "author": {
      "id": 2,
      "username": "janedoe",
      "email": "jane@example.com",
      "bio": "Designer",
      "profile_picture": null
    },
    "title": "Latest Design Trends",
    "content": "Here are the latest design trends for 2024...",
    "created_at": "2024-01-15T14:30:00Z",
    "updated_at": "2024-01-15T14:30:00Z"
  },
  {
    "id": 3,
    "author": {
      "id": 2,
      "username": "janedoe",
      "email": "jane@example.com",
      "bio": "Designer",
      "profile_picture": null
    },
    "title": "My Design Process",
    "content": "I wanted to share my design process...",
    "created_at": "2024-01-15T12:00:00Z",
    "updated_at": "2024-01-15T12:00:00Z"
  }
]
```

**cURL Example:**
```bash
curl -X GET http://localhost:8000/api/feed/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

**Notes:**
- Only returns posts from users that the authenticated user follows
- Posts are ordered by creation date (newest first)
- If you don't follow anyone, the feed will be empty
- The feed does not include your own posts (only posts from users you follow)

---

## Models

### User Model (useraccounts)

The custom user model extends Django's `AbstractUser` and includes additional fields for social media functionality.

**Fields:**
- `username` - Unique username (inherited from AbstractUser)
- `email` - User email address (inherited from AbstractUser)
- `password` - Hashed password (inherited from AbstractUser)
- `bio` - TextField for user biography (optional)
- `profile_picture` - ImageField for profile picture (optional)
- `following` - ManyToManyField to self, representing users that this user follows

**Following Relationship:**
- The `following` field is a self-referential ManyToManyField with `related_name='followers'`
- This allows bidirectional access:
  - `user.following.all()` - Returns all users that this user follows
  - `user.followers.all()` - Returns all users who follow this user (via related_name)
- The relationship is asymmetrical (`symmetrical=False`), meaning if User A follows User B, User B does not automatically follow User A

**Example Usage:**
```python
# User A follows User B
user_a.following.add(user_b)

# Now:
user_a.following.all()  # Returns [user_b] - who A follows
user_b.followers.all()  # Returns [user_a] - who follows B

# User A unfollows User B
user_a.following.remove(user_b)
```

**Model Changes:**
- Added `following` field as a ManyToManyField to enable user-to-user following relationships
- The field uses `related_name='followers'` to provide reverse access to see who follows a user
- Migration: `0002_remove_useraccounts_followers_useraccounts_following`

### Post Model

**Fields:**
- `id` - Primary key (auto-generated)
- `author` - ForeignKey to useraccounts (required)
- `title` - CharField, max 200 characters (required)
- `content` - TextField (required)
- `created_at` - DateTimeField (auto-set on creation)
- `updated_at` - DateTimeField (auto-updated on modification)

### Comment Model

**Fields:**
- `id` - Primary key (auto-generated)
- `post` - ForeignKey to Post (required)
- `author` - ForeignKey to useraccounts (required)
- `content` - TextField (required)
- `created_at` - DateTimeField (auto-set on creation)
- `updated_at` - DateTimeField (auto-updated on modification)

---

## Error Handling

### Authentication Errors

**401 Unauthorized** - Missing or invalid token:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

or

```json
{
  "detail": "Invalid token."
}
```

### Permission Errors

**403 Forbidden** - User doesn't have permission:
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### Validation Errors

**400 Bad Request** - Invalid input data:
```json
{
  "title": [
    "Title cannot be empty."
  ],
  "content": [
    "Content cannot be empty."
  ]
}
```

### Not Found Errors

**404 Not Found** - Resource doesn't exist:
```json
{
  "detail": "Not found."
}
```

---

## Summary of Endpoints

### Authentication
- `POST /api/accounts/register/` - Register a new user
- `POST /api/accounts/login/` - Login and get token

### User Management
- `POST /api/accounts/follow/<int:user_id>/` - Follow a user
- `POST /api/accounts/unfollow/<int:user_id>/` - Unfollow a user

### Posts
- `GET /api/posts/` - List all posts
- `POST /api/posts/` - Create a new post
- `GET /api/posts/{id}/` - Retrieve a specific post
- `PUT /api/posts/{id}/` - Full update a post (owner only)
- `PATCH /api/posts/{id}/` - Partial update a post (owner only)
- `DELETE /api/posts/{id}/` - Delete a post (owner only)

### Comments
- `GET /api/comments/` - List all comments
- `POST /api/comments/` - Create a new comment
- `GET /api/comments/{id}/` - Retrieve a specific comment
- `PUT /api/comments/{id}/` - Full update a comment (owner only)
- `PATCH /api/comments/{id}/` - Partial update a comment (owner only)
- `DELETE /api/comments/{id}/` - Delete a comment (owner only)

### Feed
- `GET /api/feed/` - Get personalized feed (posts from followed users)

---

## Notes

- All timestamps are in ISO 8601 format (UTC)
- The `author` field in posts and comments is automatically set to the authenticated user and cannot be modified
- The `id`, `author`, `created_at`, and `updated_at` fields are read-only
- Posts and comments are ordered by creation date (newest first)
- Users can view all posts and comments, but can only modify their own content
- Users can only modify their own following list (follow/unfollow operations)
- Users cannot follow themselves
- The feed only shows posts from users you follow, not your own posts
- Following relationships are one-way (asymmetrical) - if A follows B, B does not automatically follow A