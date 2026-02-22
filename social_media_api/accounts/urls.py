from django.urls import path
from .views import UserAccountRegisterView, UserAccountLoginView

urlpatterns = [
    path('register/', UserAccountRegisterView.as_view(), name='register'),
    path('login/', UserAccountLoginView.as_view(), name='login'),
    path('profile/', UserAccountProfileView.as_view(), name='profile'),
    path('profile/update/', UserAccountProfileUpdateView.as_view(), name='profile-update'),
    path('profile/delete/', UserAccountProfileDeleteView.as_view(), name='profile-delete'),
    path('profile/password/', UserAccountPasswordView.as_view(), name='password'),
    path('profile/password/update/', UserAccountPasswordUpdateView.as_view(), name='password-update'),
    path('profile/password/delete/', UserAccountPasswordDeleteView.as_view(), name='password-delete'),
    path('profile/password/reset/', UserAccountPasswordResetView.as_view(), name='password-reset'),
    path('profile/password/reset/confirm/', UserAccountPasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('profile/password/reset/complete/', UserAccountPasswordResetCompleteView.as_view(), name='password-reset-complete'),
]
