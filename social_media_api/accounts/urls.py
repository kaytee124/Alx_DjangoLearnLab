from django.urls import path
from .views import UserAccountRegisterView, UserAccountLoginView

urlpatterns = [
    path('register/', UserAccountRegisterView.as_view(), name='register'),
    path('login/', UserAccountLoginView.as_view(), name='login'),

]
