from django.shortcuts import render
from .models import Book, Author, Library, Librarian
from django.http import HttpResponse

# Create your views here.
def book_list(request):
    books = Book.objects.all()
    book_list = []
    for book in books:
        book_list.append(f"{book.title} by {book.author.name}")
    return render(request, 'list_books.html', {'books': book_list})

class LibraryListView(ListView):
    model = Library
    template_name = 'library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all()
        return context