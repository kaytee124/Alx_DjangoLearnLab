from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(APIView):
    """
    View to fetch all notifications for the authenticated user.
    Unread notifications are shown prominently (ordered first).
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NotificationSerializer

    def get(self, request):
        user = request.user
        # Get all notifications, unread first
        notifications = Notification.objects.filter(recipient=user).order_by('read', '-timestamp')
        serializer = self.serializer_class(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class NotificationMarkReadView(APIView):
    """
    View to mark a notification as read.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, notification_id):
        user = request.user
        notification = Notification.objects.filter(id=notification_id, recipient=user).first()
        
        if not notification:
            return Response(
                {'error': 'Notification not found.'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        if notification.read == True:
            return Response(
                {'error': 'Notification already read.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        notification.read = True
        notification.save()
        
        return Response(
            {'message': 'Notification marked as read.'}, 
            status=status.HTTP_200_OK
        )

class NotificationUnreadCountView(APIView):
    """
    View to get the count of unread notifications.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        unread_count = Notification.objects.filter(recipient=user, read=False).count()
        return Response({'unread_count': unread_count}, status=status.HTTP_200_OK)
