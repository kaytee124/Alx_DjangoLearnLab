from rest_framework import viewsets, permissions
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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


class FeedView(APIView):
    """
    View to generate a feed based on posts from users that the current user follows.
    Returns posts ordered by creation date, showing the most recent posts at the top.
    """
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        following_users = user.following.all()
        
        # Get posts from users that the current user follows
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        
        serializer = self.serializer_class(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

