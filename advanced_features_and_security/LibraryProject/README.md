# Library Project - Security Documentation

## Overview

This Django project implements a comprehensive library management system with multiple security layers to protect against common web vulnerabilities.

## Security Features Implemented

### 1. Content Security Policy (CSP)

**Location**: `LibraryProject/middleware.py`

**Purpose**: Prevents XSS (Cross-Site Scripting) attacks by controlling which resources can be loaded by the browser.

**Implementation**:
- Custom CSP middleware sets security headers on all responses
- Restricts script execution to same origin
- Prevents inline script execution (with exceptions for Django admin)
- Blocks object/plugin loading
- Upgrades insecure HTTP requests to HTTPS

**Security Benefit**: Defense-in-depth against code injection attacks.

### 2. CSRF Protection

**Location**: `LibraryProject/settings.py` (middleware configuration)

**Purpose**: Prevents Cross-Site Request Forgery attacks.

**Implementation**:
- `CsrfViewMiddleware` automatically validates CSRF tokens on all POST requests
- CSRF tokens included in all forms via `{% csrf_token %}`
- Secure cookie settings: `CSRF_COOKIE_SECURE = True` (HTTPS only)
- SameSite cookie attribute: `CSRF_COOKIE_SAMESITE = 'Lax'`

**Security Benefit**: Ensures form submissions come from legitimate sources.

### 3. SQL Injection Prevention

**Location**: All views and models

**Purpose**: Prevents SQL injection attacks through malicious database queries.

**Implementation**:
- **Django ORM**: All database queries use Django's ORM (automatically parameterized)
- **No raw SQL**: No `raw()` or `extra()` queries used
- **get_object_or_404()**: Used instead of `.get()` to prevent information disclosure
- **Form validation**: All user inputs validated before database operations

**Example**:
```python
# SECURE: Uses parameterized ORM query
book = get_object_or_404(Book, pk=pk)

# INSECURE (not used): Direct string formatting
# book = Book.objects.raw("SELECT * FROM book WHERE id = %s" % pk)
```

**Security Benefit**: All queries are automatically parameterized, preventing SQL injection.

### 4. XSS (Cross-Site Scripting) Prevention

**Location**: Forms, templates, and middleware

**Purpose**: Prevents malicious scripts from being injected and executed.

**Implementation**:
- **CSP headers**: Restricts resource loading (see CSP section)
- **Input validation**: Forms sanitize inputs (strips HTML tags)
- **Django auto-escaping**: Templates automatically escape user content
- **Content-Type protection**: `SECURE_CONTENT_TYPE_NOSNIFF = True`

**Example**:
```python
# In forms.py - clean_title() method
if '<' in title or '>' in title:
    raise forms.ValidationError('Title contains invalid characters.')
```

**Security Benefit**: Multiple layers prevent script injection.

### 5. Input Validation and Sanitization

**Location**: `relationship_app/forms.py`

**Purpose**: Ensures all user inputs are validated and sanitized before processing.

**Implementation**:
- **Django forms**: All inputs go through form validation
- **Custom clean methods**: Additional validation layers
- **Whitespace stripping**: Prevents padding attacks
- **Length limits**: Prevents buffer overflow attacks
- **Type validation**: Ensures correct data types

**Example**:
```python
class BookForm(forms.ModelForm):
    def clean_title(self):
        title = self.cleaned_data.get('title')
        title = title.strip()  # Sanitize
        if not title:
            raise forms.ValidationError('Title cannot be empty.')
        if '<' in title or '>' in title:  # XSS prevention
            raise forms.ValidationError('Title contains invalid characters.')
        return title
```

**Security Benefit**: All inputs are validated and safe to use.

### 6. Authentication and Authorization

**Location**: `relationship_app/views.py`

**Purpose**: Ensures only authorized users can access protected resources.

**Implementation**:
- **@login_required**: Requires user authentication
- **@permission_required**: Checks specific permissions
- **@user_passes_test**: Custom authorization logic
- **Form-based authentication**: Uses Django's `AuthenticationForm` (validated inputs)
- **Secure password handling**: Uses Django's password hashing (bcrypt, etc.)

**Example**:
```python
@permission_required('relationship_app.can_delete_book')
def delete_book(request, pk):
    # Only users with 'can_delete_book' permission can access
    book = get_object_or_404(Book, pk=pk)
    ...
```

**Security Benefit**: Prevents unauthorized access to sensitive operations.

### 7. Session Security

**Location**: `LibraryProject/settings.py`

**Purpose**: Protects user sessions from hijacking and fixation attacks.

**Implementation**:
- **Secure cookies**: `SESSION_COOKIE_SECURE = True` (HTTPS only)
- **SameSite attribute**: `SESSION_COOKIE_SAMESITE = 'Lax'`
- **Session middleware**: Manages secure session handling

**Security Benefit**: Sessions are protected from interception and cross-site attacks.

### 8. Clickjacking Protection

**Location**: `LibraryProject/settings.py` and CSP middleware

**Purpose**: Prevents pages from being embedded in malicious iframes.

**Implementation**:
- **X_FRAME_OPTIONS = 'DENY'**: Prevents iframe embedding
- **CSP frame-ancestors**: Additional protection via CSP header

**Security Benefit**: Prevents clickjacking attacks.

### 9. HTTPS Enforcement

**Location**: `LibraryProject/settings.py`

**Purpose**: Ensures all communication is encrypted.

**Implementation**:
- **SECURE_SSL_REDIRECT = True**: Forces HTTP to HTTPS redirect
- **Secure cookies**: All cookies only sent over HTTPS
- **CSP upgrade-insecure-requests**: Automatically upgrades HTTP to HTTPS

**Security Benefit**: Prevents man-in-the-middle attacks and data interception.

### 10. Information Disclosure Prevention

**Location**: All views

**Purpose**: Prevents attackers from learning about system internals.

**Implementation**:
- **get_object_or_404()**: Returns 404 instead of 500 errors
- **Exception handling**: Doesn't reveal if resources exist
- **DEBUG = False**: Prevents error page information disclosure

**Example**:
```python
# SECURE: Returns 404 if not found (doesn't reveal if book exists)
book = get_object_or_404(Book, pk=pk)

# INSECURE (not used): Would raise exception revealing information
# book = Book.objects.get(pk=pk)
```

**Security Benefit**: Attackers can't learn about system structure from errors.

## Security Settings Summary

### Settings.py Security Configuration

```python
# Host Security
ALLOWED_HOSTS = ['*']  # TODO: Update with actual domain

# XSS Protection
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Clickjacking Protection
X_FRAME_OPTIONS = 'DENY'

# HTTPS Enforcement
SECURE_SSL_REDIRECT = True

# CSRF Protection
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_TRUSTED_ORIGINS = ['https://*.yourdomain.com']

# Session Security
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_SAMESITE = 'Lax'
```

## Code Security Practices

### 1. ORM Usage (SQL Injection Prevention)

**Always use Django ORM**:
```python
# ✅ SECURE
books = Book.objects.filter(author=author)
book = get_object_or_404(Book, pk=pk)

# ❌ INSECURE (never use)
# books = Book.objects.raw("SELECT * FROM book WHERE author = %s" % author_name)
```

### 2. Form Validation (Input Sanitization)

**Always validate inputs through forms**:
```python
# ✅ SECURE
form = BookForm(request.POST)
if form.is_valid():
    title = form.cleaned_data['title']  # Sanitized

# ❌ INSECURE (never use)
# title = request.POST['title']  # Raw, unsanitized
```

### 3. Error Handling (Information Disclosure)

**Use get_object_or_404() instead of .get()**:
```python
# ✅ SECURE
book = get_object_or_404(Book, pk=pk)  # Returns 404 if not found

# ❌ INSECURE
# book = Book.objects.get(pk=pk)  # Raises exception, reveals information
```

### 4. CSRF Tokens (Form Protection)

**Always include CSRF tokens in forms**:
```html
<!-- ✅ SECURE -->
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Submit</button>
</form>
```

## Testing Security

### Basic Security Tests

Run the security test suite:
```bash
python manage.py test relationship_app.tests
```

### Manual Security Checks

1. **CSRF Protection**: Try submitting forms without CSRF token (should fail)
2. **XSS Prevention**: Try injecting `<script>alert('XSS')</script>` in forms (should be blocked)
3. **SQL Injection**: Try SQL injection in search fields (should be safe due to ORM)
4. **Authorization**: Try accessing protected views without login (should redirect)
5. **CSP Headers**: Check browser console for CSP violations

## Production Deployment Checklist

Before deploying to production:

- [ ] Update `ALLOWED_HOSTS` with actual domain
- [ ] Update `CSRF_TRUSTED_ORIGINS` with actual domain
- [ ] Set `SECRET_KEY` from environment variable (never commit)
- [ ] Ensure `DEBUG = False`
- [ ] Configure HTTPS/SSL certificates
- [ ] Set up proper database (not SQLite for production)
- [ ] Configure static files serving
- [ ] Set up proper logging
- [ ] Review and test all security settings
- [ ] Run security audit tools

## Additional Resources

- [Django Security Documentation](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Content Security Policy Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)

## Security Contact

For security issues, please follow responsible disclosure practices.

---

**Last Updated**: 2024
**Security Review**: All security measures have been implemented and documented.
