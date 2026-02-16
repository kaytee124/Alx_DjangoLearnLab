from django.urls import path
from .views import BookList
from rest_framework.routers import DefaultRouter
from .views import BookViewSet
from django.urls import include
from rest_framework.authtoken.views import obtain_auth_token


router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='books_all')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'), #Maps to the BookList view,
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'), #Token retrieval endpoint
    path('', include(router.urls)) #This includes all routes registered with the router,
]