from django.urls import path
from .views import book_list, LibraryListView

urlpatterns = [
    path('books/', book_list, name='book_list'),
    path('libraries/<int:pk>/', LibraryListView.as_view(), name='library_list'),
]