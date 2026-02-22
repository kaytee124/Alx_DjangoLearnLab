from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, GenericAPIView
from .serializers import UserAccountRegisterSerializer, UserAccountLoginSerializer, UserAccountSerializer
from .models import useraccounts
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.shortcuts import get_object_or_404

class UserAccountRegisterView(CreateAPIView):
    queryset = useraccounts.objects.all()
    serializer_class = UserAccountRegisterSerializer

class UserAccountLoginView(APIView):
    serializer_class = UserAccountLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class FollowUserView(GenericAPIView):
    """
    View to follow a user.
    Users can only modify their own following list.
    """
    queryset = useraccounts.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        current_user = request.user
        user_to_follow = get_object_or_404(self.get_queryset(), id=user_id)
        
        # Prevent users from following themselves
        if current_user == user_to_follow:
            return Response(
                {'error': 'You cannot follow yourself.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if already following
        if current_user.following.filter(id=user_id).exists():
            return Response(
                {'error': 'You are already following this user.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Add to following list
        current_user.following.add(user_to_follow)
        
        return Response(
            {
                'message': f'You are now following {user_to_follow.username}',
                'user': UserAccountSerializer(user_to_follow).data
            },
            status=status.HTTP_200_OK
        )

class UnfollowUserView(GenericAPIView):
    """
    View to unfollow a user.
    Users can only modify their own following list.
    """
    queryset = useraccounts.objects.all()
    serializer_class = UserAccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        current_user = request.user
        user_to_unfollow = get_object_or_404(self.get_queryset(), id=user_id)
        
        # Check if currently following
        if not current_user.following.filter(id=user_id).exists():
            return Response(
                {'error': 'You are not following this user.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Remove from following list
        current_user.following.remove(user_to_unfollow)
        
        return Response(
            {
                'message': f'You have unfollowed {user_to_unfollow.username}',
                'user': UserAccountSerializer(user_to_unfollow).data
            },
            status=status.HTTP_200_OK
        )

