from django.urls import path
from .views import (
    UserAccountRegisterView, 
    UserAccountLoginView, 
    FollowUserView, 
    UnfollowUserView
)

urlpatterns = [
    path('register/', UserAccountRegisterView.as_view(), name='register'),
    path('login/', UserAccountLoginView.as_view(), name='login'),
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow'),
]
