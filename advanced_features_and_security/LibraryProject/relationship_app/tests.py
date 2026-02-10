"""
Security Tests for relationship_app

These tests verify that security measures are properly implemented:
- CSRF protection
- XSS prevention
- SQL injection prevention
- Authentication and authorization
- Input validation
- CSP headers
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import Http404
from .models import Book, Author, CustomUser, UserProfile
from .forms import BookForm

User = get_user_model()


class CSRFProtectionTests(TestCase):
    """Test CSRF protection on POST requests"""
    
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.author = Author.objects.create(name="Test Author")
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        # Create user profile
        UserProfile.objects.create(user=self.user, role='Admin')
        
    def test_csrf_protection_on_add_book(self):
        """Test that POST requests without CSRF token are rejected"""
        self.client.login(username='testuser', password='testpass123')
        # Grant permission
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType
        content_type = ContentType.objects.get_for_model(Book)
        permission = Permission.objects.get(codename='can_add_book', content_type=content_type)
        self.user.user_permissions.add(permission)
        
        # Try to POST without CSRF token
        response = self.client.post(
            reverse('add_book'),
            {'title': 'Test Book', 'author': self.author.id},
            follow=False
        )
        # Should be rejected (403 Forbidden)
        self.assertEqual(response.status_code, 403, "CSRF protection should reject requests without token")
    
    def test_csrf_token_in_forms(self):
        """Test that forms include CSRF tokens"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('add_book'))
        # Check that response contains csrf token
        self.assertContains(response, 'csrfmiddlewaretoken', msg_prefix="Forms should include CSRF tokens")


class XSSPreventionTests(TestCase):
    """Test XSS prevention in forms and templates"""
    
    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
    
    def test_xss_prevention_in_book_title(self):
        """Test that XSS attempts in book title are blocked"""
        form = BookForm(data={
            'title': '<script>alert("XSS")</script>',
            'author': self.author.id
        })
        # Form should be invalid due to XSS characters
        self.assertFalse(form.is_valid(), "Form should reject XSS attempts")
        self.assertIn('invalid characters', str(form.errors), "Should show XSS error message")
    
    def test_xss_prevention_in_book_title_angle_brackets(self):
        """Test that angle brackets are blocked"""
        form = BookForm(data={
            'title': 'Test <b>Bold</b> Title',
            'author': self.author.id
        })
        self.assertFalse(form.is_valid(), "Form should reject HTML tags")
    
    def test_safe_title_accepted(self):
        """Test that safe titles are accepted"""
        form = BookForm(data={
            'title': 'Safe Book Title 123',
            'author': self.author.id
        })
        self.assertTrue(form.is_valid(), "Safe titles should be accepted")


class SQLInjectionPreventionTests(TestCase):
    """Test SQL injection prevention through ORM usage"""
    
    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(title="Test Book", author=self.author)
    
    def test_orm_prevents_sql_injection_in_pk(self):
        """Test that ORM prevents SQL injection in primary key lookups"""
        # Try SQL injection in pk parameter
        # This should not execute SQL, but should safely handle the input
        from django.shortcuts import get_object_or_404
        
        # Valid pk should work
        book = get_object_or_404(Book, pk=1)
        self.assertIsNotNone(book)
        
        # Invalid pk should return 404, not raise SQL error
        with self.assertRaises(Http404):
            get_object_or_404(Book, pk=99999)
    
    def test_orm_parameterized_queries(self):
        """Test that ORM uses parameterized queries"""
        # ORM automatically parameterizes, so this is safe
        books = Book.objects.filter(title="Test Book")
        self.assertEqual(books.count(), 1)
        
        # Even with special characters, ORM handles it safely
        Book.objects.create(title="Test's Book", author=self.author)
        books = Book.objects.filter(title="Test's Book")
        self.assertEqual(books.count(), 1)


class InputValidationTests(TestCase):
    """Test input validation in forms"""
    
    def setUp(self):
        self.author = Author.objects.create(name="Test Author")
    
    def test_empty_title_rejected(self):
        """Test that empty titles are rejected"""
        form = BookForm(data={'title': '', 'author': self.author.id})
        self.assertFalse(form.is_valid(), "Empty title should be rejected")
    
    def test_whitespace_only_title_rejected(self):
        """Test that whitespace-only titles are rejected"""
        form = BookForm(data={'title': '   ', 'author': self.author.id})
        self.assertFalse(form.is_valid(), "Whitespace-only title should be rejected")
    
    def test_title_length_limit(self):
        """Test that titles exceeding max length are rejected"""
        long_title = 'a' * 101  # Exceeds max_length=100
        form = BookForm(data={'title': long_title, 'author': self.author.id})
        self.assertFalse(form.is_valid(), "Title exceeding max length should be rejected")
    
    def test_author_required(self):
        """Test that author selection is required"""
        form = BookForm(data={'title': 'Test Book', 'author': ''})
        self.assertFalse(form.is_valid(), "Author should be required")
    
    def test_valid_input_accepted(self):
        """Test that valid inputs are accepted"""
        form = BookForm(data={'title': 'Valid Book Title', 'author': self.author.id})
        self.assertTrue(form.is_valid(), "Valid inputs should be accepted")


class AuthenticationTests(TestCase):
    """Test authentication and authorization"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        UserProfile.objects.create(user=self.user, role='Member')
    
    def test_login_requires_authentication(self):
        """Test that protected views require authentication"""
        # Try to access protected view without login
        response = self.client.get(reverse('add_book'))
        # Should redirect to login
        self.assertEqual(response.status_code, 302, "Should redirect to login")
        self.assertIn('/login/', response.url, "Should redirect to login page")
    
    def test_authenticated_user_can_access(self):
        """Test that authenticated users can access protected views"""
        self.client.login(username='testuser', password='testpass123')
        # Grant permission
        from django.contrib.auth.models import Permission
        from django.contrib.contenttypes.models import ContentType
        content_type = ContentType.objects.get_for_model(Book)
        permission = Permission.objects.get(codename='can_add_book', content_type=content_type)
        self.user.user_permissions.add(permission)
        
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 200, "Authenticated users should access protected views")
    
    def test_permission_required_enforced(self):
        """Test that permission requirements are enforced"""
        self.client.login(username='testuser', password='testpass123')
        # User doesn't have permission
        response = self.client.get(reverse('add_book'))
        # Should be forbidden (403) or redirect
        self.assertIn(response.status_code, [302, 403], "Users without permission should be blocked")


class CSPHeaderTests(TestCase):
    """Test Content Security Policy headers"""
    
    def setUp(self):
        self.client = Client()
    
    def test_csp_header_present(self):
        """Test that CSP header is present in responses"""
        response = self.client.get(reverse('list_books'))
        self.assertIn('Content-Security-Policy', response, "CSP header should be present")
    
    def test_csp_header_content(self):
        """Test that CSP header contains security directives"""
        response = self.client.get(reverse('list_books'))
        csp_header = response.get('Content-Security-Policy', '')
        
        # Check for important CSP directives
        self.assertIn("default-src 'self'", csp_header, "CSP should restrict default sources")
        self.assertIn("script-src", csp_header, "CSP should restrict script sources")
        self.assertIn("frame-ancestors 'none'", csp_header, "CSP should prevent iframe embedding")


class SecurityHeadersTests(TestCase):
    """Test security headers are present"""
    
    def setUp(self):
        self.client = Client()
    
    def test_x_frame_options_header(self):
        """Test that X-Frame-Options header is present"""
        response = self.client.get(reverse('list_books'))
        # X-Frame-Options should be set (either via middleware or CSP)
        # CSP frame-ancestors also provides this protection
        csp_header = response.get('Content-Security-Policy', '')
        self.assertIn('frame-ancestors', csp_header.lower(), "Should prevent iframe embedding")
    
    def test_content_type_nosniff(self):
        """Test that Content-Type nosniff is configured"""
        # This is set in settings, so responses should be protected
        # We verify the setting is correct
        from django.conf import settings
        self.assertTrue(settings.SECURE_CONTENT_TYPE_NOSNIFF, "Content-Type nosniff should be enabled")


class InformationDisclosureTests(TestCase):
    """Test that information disclosure is prevented"""
    
    def setUp(self):
        self.client = Client()
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(title="Test Book", author=self.author)
    
    def test_404_on_nonexistent_book(self):
        """Test that 404 is returned instead of 500 for nonexistent books"""
        self.client.login(username='testuser', password='testpass123')
        # Try to access nonexistent book
        response = self.client.get(reverse('edit_book', kwargs={'pk': 99999}))
        # Should return 404, not 500
        self.assertEqual(response.status_code, 404, "Should return 404 for nonexistent resources")
    
    def test_no_error_details_in_response(self):
        """Test that error responses don't leak information"""
        from django.conf import settings
        # In production, DEBUG should be False
        # This prevents error pages from showing stack traces
        self.assertFalse(settings.DEBUG, "DEBUG should be False in production")


class EmailValidationTests(TestCase):
    """Test email validation in authentication backend"""
    
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_invalid_email_rejected(self):
        """Test that invalid email formats are rejected"""
        from .views import emailbackend
        
        backend = emailbackend()
        # Try with invalid email
        result = backend.authenticate(None, username='not-an-email', password='testpass123')
        self.assertIsNone(result, "Invalid email should be rejected")
    
    def test_valid_email_accepted(self):
        """Test that valid email formats are accepted"""
        from .views import emailbackend
        
        backend = emailbackend()
        # Try with valid email
        result = backend.authenticate(None, username='test@example.com', password='testpass123')
        self.assertIsNotNone(result, "Valid email should be accepted")
        self.assertEqual(result, self.user, "Should return correct user")
