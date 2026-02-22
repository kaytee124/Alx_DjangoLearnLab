from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from .serializers import UserAccountRegisterSerializer, UserAccountLoginSerializer
from .models import useraccounts
from rest_framework.response import Response
from rest_framework import status

class UserAccountRegisterView(CreateAPIView):
    queryset = useraccounts.objects.all()
    serializer_class = UserAccountRegisterSerializer

class UserAccountLoginView(APIView):
    serializer_class = UserAccountLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

