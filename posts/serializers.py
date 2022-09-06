from rest_framework import serializers
from .models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'user',
            'created_at'
        ]

class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'desc',
            'posted_at',
            'user',
            'image'
        ]

class PostDetailSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'desc',
            'posted_at',
            'image',
            'comments'
        ]