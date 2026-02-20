from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list.as_view(), name='book-list'),
    path('books/<int:pk>/', views.book_detail.as_view(), name='book-detail'),
    path('books/create/', views.create_book.as_view(), name='create-book'),
    path('books/<int:pk>/update/', views.update_book.as_view(), name='update-book'),
    path('books/<int:pk>/delete/', views.delete_book.as_view(), name='delete-book'),
]