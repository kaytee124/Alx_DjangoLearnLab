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
from .forms import BookForm, ExampleForm

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.backends import BaseBackend

# Create your views here.
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookshelf/list_books.html', {'books': books})


# admins and Editors can add books
@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'bookshelf/add_book.html', {'form': form})

# Editors and Admins can edit books
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'bookshelf/edit_book.html', {'form': form})

# Admins can delete books
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'bookshelf/delete_book.html', {'book': book})


# Example form view
def form_example(request):
    """
    Example view demonstrating form usage
    
    This view shows how to handle form submissions with proper validation
    and security measures.
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            # In a real application, you would save this data or send an email
            # For this example, we'll just show a success message
            return render(request, 'bookshelf/form_example.html', {
                'form': ExampleForm(),
                'success': True,
                'submitted_data': {
                    'name': name,
                    'email': email,
                    'message': message
                }
            })
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/form_example.html', {'form': form})



