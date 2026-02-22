from rest_framework import viewsets, permissions, generics
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification

# Add get_object_or_404 to generics module
generics.get_object_or_404 = get_object_or_404


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
    Creates notifications when comments are created.
    """
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def perform_create(self, serializer):
        comment = serializer.save()
        # Create notification for post author (if not commenting on own post)
        if comment.post.author != comment.author:
            Notification.objects.create(
                recipient=comment.post.author,
                actor=comment.author,
                verb='commented on your post',
                target=comment.post
            )


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

class LikePostView(APIView):
    """
    View to like a post.
    Checks for authentication and prevents users from liking a post multiple times.
    Creates a notification for the post author.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        current_user = request.user
        post = generics.get_object_or_404(Post, pk=pk)
        
        # Check if user is trying to like their own post
        if post.author == current_user:
            return Response(
                {'error': 'You cannot like your own post.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get or create the like (get_or_create prevents duplicates)
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if not created:
            return Response(
                {'error': 'You have already liked this post.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create notification for post author
        Notification.objects.create(
            recipient=post.author,
            actor=current_user,
            verb='liked your post',
            target=post
        )
        
        return Response(
            {'message': 'You have liked this post.'}, 
            status=status.HTTP_200_OK
        )


class UnlikePostView(APIView):
    """
    View to unlike a post.
    Checks for authentication and prevents users from unliking a post they haven't liked.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        current_user = request.user
        post = generics.get_object_or_404(Post, pk=pk)
        
        # Check if user has liked this post
        like = Like.objects.filter(post=post, user=current_user).first()
        if not like:
            return Response(
                {'error': 'You have not liked this post.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Delete the like
        like.delete()
        
        return Response(
            {'message': 'You have unliked this post.'}, 
            status=status.HTTP_200_OK
        )