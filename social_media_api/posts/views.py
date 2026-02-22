from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit or delete it.
    Read permissions are allowed to any authenticated user.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Write permissions (create, update, delete) are only allowed to the owner
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Post instances.
    Provides CRUD operations: Create, Read, Update, Delete
    """
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing Comment instances.
    Provides CRUD operations: Create, Read, Update, Delete
    """
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
