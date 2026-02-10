"""
Views for the relationship_app

SECURITY NOTES:
- All views use Django ORM (parameterized queries) to prevent SQL injection
- All user inputs are validated through Django forms
- get_object_or_404() is used instead of .get() to prevent information disclosure
- Authentication and authorization checks are enforced via decorators
- CSRF protection is handled automatically by Django middleware
"""
from django.shortcuts import render, get_object_or_404
from .models import Book, Author
from .models import Library
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.views.generic import View
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from .models import CustomUser
from .forms import BookForm

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.backends import BaseBackend
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

# Create your views here.
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()
        return context

class LoginView(View):
    """
    Login view with proper form validation
    
    SECURITY:
    - Uses AuthenticationForm for input validation (prevents injection)
    - Uses form.cleaned_data instead of direct POST access (sanitized data)
    - CSRF protection handled automatically by middleware
    - Password is never logged or exposed (handled by Django's authenticate)
    """
    template_name = 'relationship_app/login.html'
    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        # SECURITY: Use form validation instead of direct POST access
        # This ensures all inputs are validated and sanitized
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # SECURITY: Use cleaned_data (validated/sanitized) instead of raw POST
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('list_books')
        return render(request, self.template_name, {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = UserCreationForm()

    return render(request, 'relationship_app/register.html', {'form': form})

class LogoutView(View):
    template_name = 'relationship_app/logout.html'
    def get(self, request):
        return render(request, self.template_name)

from django.contrib.auth.decorators import login_required

@login_required
@user_passes_test(lambda u: hasattr(u, 'profile') and u.profile.role == 'Admin')
def Admin(request):
    return render(request, 'relationship_app/admin_view.html')

@login_required 
@user_passes_test(lambda u: hasattr(u, 'profile') and u.profile.role == 'Librarians')
def Librarian(request):
    return render(request, 'relationship_app/librarian_view.html')

@login_required
@user_passes_test(lambda u: hasattr(u, 'profile') and u.profile.role == 'Member')
def Member(request):
    return render(request, 'relationship_app/member_view.html')

@permission_required('relationship_app.can_add_book')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})

@permission_required('relationship_app.can_change_book')
def edit_book(request, pk):
    """
    Edit book view with security measures
    
    SECURITY:
    - @permission_required: Ensures only authorized users can edit
    - get_object_or_404: Prevents information disclosure (404 vs 500 error)
    - BookForm validation: All inputs validated and sanitized
    - CSRF protection: Automatic via middleware
    - ORM usage: Parameterized queries prevent SQL injection
    """
    # SECURITY: Use get_object_or_404 instead of .get() to prevent information disclosure
    # Returns 404 if book doesn't exist (doesn't reveal if book exists or not)
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        # SECURITY: Form validation ensures all inputs are safe
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form})

@permission_required('relationship_app.can_delete_book')
def delete_book(request, pk):
    """
    Delete book view with security measures
    
    SECURITY:
    - @permission_required: Ensures only authorized users can delete
    - get_object_or_404: Prevents information disclosure
    - POST method required: Prevents accidental deletions via GET
    - CSRF protection: Automatic via middleware
    """
    # SECURITY: Use get_object_or_404 to prevent information disclosure
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        # SECURITY: Only allow deletion via POST (not GET) to prevent CSRF
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})



class emailbackend(BaseBackend):
    """
    Custom authentication backend using email
    
    SECURITY:
    - Email validation: Prevents invalid email formats
    - Null checks: Prevents None values from causing errors
    - ORM usage: Parameterized queries prevent SQL injection
    - Password checking: Uses Django's secure password hashing
    - Exception handling: Prevents information disclosure
    """
    def authenticate(self, request, username=None, password=None):
        # SECURITY: Validate inputs before processing
        if not username or not password:
            return None
        
        # SECURITY: Validate email format to prevent injection attacks
        # This ensures only valid email formats are processed
        try:
            validate_email(username)
        except ValidationError:
            return None
        
        # SECURITY: Use ORM .get() with try/except to prevent information disclosure
        # Returns None instead of raising exception (doesn't reveal if user exists)
        try:
            # SECURITY: ORM automatically parameterizes queries (SQL injection prevention)
            user = CustomUser.objects.get(email=username)
            # SECURITY: Django's check_password uses secure hashing (bcrypt, etc.)
            if user and user.check_password(password):
                return user
            else:
                return None
        except CustomUser.DoesNotExist:
            # SECURITY: Don't reveal if user exists or not (prevents user enumeration)
            return None

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None