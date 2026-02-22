from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html', http_method_names=['get', 'post']), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='blog/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='blog/password_reset_done.html'), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='blog/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='blog/password_reset_complete.html'), name='password_reset_complete'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('', views.ListView.as_view(), name='post_list'),
    path('home/', views.ListView.as_view(), name='home'),  # Alias for base template
    path('posts/', views.ListView.as_view(), name='posts'),  # Alias for base template
    path('post/<int:pk>/', views.DetailView.as_view(), name='post_detail'),
    path('post/new/', views.CreateView.as_view(), name='post_create'),
    path('post/<int:pk>/edit/', views.UpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.DeleteView.as_view(), name='post_delete'),
]