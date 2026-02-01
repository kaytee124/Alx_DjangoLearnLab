from django.shortcuts import render
from .models import Book, Author
from .models import Library
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth import logout


# Create your views here.
def list_books(request):
    books = Book.objects.all()
    return render(request, 'templates/relationship_app/list_books.html', {'books': books})

class LibraryDetailView(DetailView):
    model = Library
    template_name = 'templates/relationship_app/library_detail.html'
    context_object_name = 'library'

    def render_to_response(self, context):
        library = self.get_object()
        books = library.books.all()
        return render(self.request, 'templates/relationship_app/library_detail.html', {'library': library, 'books': books})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse('Login successful')
        else:
            return render(request, 'templates/relationship_app/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'templates/relationship_app/login.html',{'Error': "Invalid request method"})

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()
        login(request, user)
        return HttpResponse('User created successfully')
    else:
        return render(request, 'templates/relationship_app/register.html', {'Error': "Invalid request method"})
    
def logout(request):
    logout(request)
    return HttpResponse('Logged out successfully')