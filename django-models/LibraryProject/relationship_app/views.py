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
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect


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

class LoginView(View):
    template_name = 'templates/relationship_app/login.html'
    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list_books')
        else:
            return render(request, self.template_name, {'error': 'Invalid username or password'})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            login(request, form.instance)
            return HttpResponse('User created successfully')
        else:
            return render(request, 'templates/relationship_app/register.html', {'form': form})
    else:
        return render(request, 'templates/relationship_app/register.html', {'Error': "Invalid request method"})
    
class LogoutView(View):
    template_name = 'templates/relationship_app/logout.html'
    def get(self, request):
        return render(request, self.template_name)