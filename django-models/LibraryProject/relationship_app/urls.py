from django.urls import path
from .views import list_books
from .views import LibraryDetailView
from .views import LoginView
from . import views
from .views import LogoutView
urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('libraries/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('login/', LoginView.as_view(template_name='templates/relationship_app/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(template_name='templates/relationship_app/logout.html'), name='logout'),
]