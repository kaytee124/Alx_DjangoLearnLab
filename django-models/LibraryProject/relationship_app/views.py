from django.shortcuts import render
from .models import Book, Author
from .models import Library
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView


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