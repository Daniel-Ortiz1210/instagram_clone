from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, UserProfileSerializer, FollowingSerializer, FollowersSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Follow

class RegisterUser(APIView):

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfile(APIView):
    permissions_classes = [IsAuthenticated]

    def get(self, request, username):
        if username == request.user.username:
            serializer = UserProfileSerializer(request.user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, username):
        if username == request.user.username:
            serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class Following(APIView):
    permissions_classes = [IsAuthenticated]

    def get(self, request, username):
        if username == request.user.username:
            q = Follow.objects.filter(from_user=request.user).all()
            serializer = FollowSerializer(q, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


class Followers(APIView):

    permissions_classes = [IsAuthenticated]

    def get(self, request, username):
        if username == request.user.username:
            q = Follow.objects.filter(to_user=request.user).all()
            serializer = FollowersSerializer(q, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)