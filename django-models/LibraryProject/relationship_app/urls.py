from django.urls import path
from .views import list_books
from .views import LibraryDetailView
from .views import LoginView
from . import views
from .views import LogoutView
from .views import Admin
from .views import Librarian
from .views import Member

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('admin/', Admin, name='admin'),
    path('librarian/', Librarian, name='librarian'),
    path('member/', Member, name='member'),
    path('add_book/', add_book, name='add_book'),
    path('edit_book/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),
]