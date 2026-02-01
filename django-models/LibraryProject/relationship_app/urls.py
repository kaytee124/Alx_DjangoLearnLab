from django.urls import path
from .views import list_books
from .views import LibraryDetailView
from .views import login
from .views import register
from .views import logout
urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
]