from django.urls import path
from .views import list_books
from .views import LibraryDetailView

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('libraries/<int:pk>/', LibraryListView.as_view(), name='library_list'),
]