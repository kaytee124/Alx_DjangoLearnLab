from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='list_books'),
    path('form_example/', views.form_example, name='form_example'),
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),
]
