from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Post, Comment
from .serializers import PostsSerializer, PostDetailSerializer, CommentSerializer
from django.shortcuts import get_object_or_404

class CreatePostView(APIView):
    
    permissions_classes = [IsAuthenticated]

    def post(self, request, username):
        if username == request.user.username:
            desc = request.data['desc']
            image = request.data['image']
            user = request.user
            post = Post.objects.create(desc=desc, image=image, user=user)
            serializer = PostsSerializer(post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    

class PostView(APIView):

    permissions_classes = [IsAuthenticated]

    def get(self, request, id):
        post = get_object_or_404(Post, id=id)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
       
    def patch(self, request, id):
        post = get_object_or_404(Post, id=id)
        if post.user.username == request.user.username:
            serializer = PostDetailSerializer(post, request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, id):
        post = get_object_or_404(Post, id=id)
        if post.user.username == request.user.username:
            post.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class CommentsView(APIView):

    permissions_classes = [IsAuthenticated]

    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = CommentSerializer(post.comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        try:
            comment = Comment(content=request.data['content'], post=post, user=request.user)
            comment.save()
            post.comments.add(comment)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_201_CREATED)