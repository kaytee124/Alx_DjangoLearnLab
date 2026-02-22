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
    path('', views.PostListView.as_view(), name='post_list'),
    path('home/', views.PostListView.as_view(), name='home'),  # Alias for base template
    path('posts/', views.PostListView.as_view(), name='posts'),  # Alias for base template
    path('search/', views.PostListView.as_view(), name='search'),  # Search uses same view with query parameter
    path('tags/<str:tag_name>/', views.TagPostListView.as_view(), name='posts_by_tag'),  # View posts by tag
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    # Comment URLs - nested under posts for better structure
    path('post/<int:pk>/comments/new/', views.CommentCreateView.as_view(), name='comment_create'),
    path('post/<int:post_id>/comments/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update'),
    path('post/<int:post_id>/comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    # Flat comment URLs (for checks/compatibility)
    path('comment/<int:pk>/update/', views.CommentUpdateView.as_view(), name='comment_update_alt'),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete_alt'),
]