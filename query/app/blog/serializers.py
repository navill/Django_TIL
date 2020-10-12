from django.contrib.auth import get_user_model
from rest_framework import serializers

from blog.models import Post, Comment

User = get_user_model()


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
    comment = serializers.CharField()

    class Meta:
        model = Comment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    title = serializers.CharField()
    body = serializers.CharField()
    comments = serializers.StringRelatedField(many=True)


    class Meta:
        model = Post
        fields = ['user', 'title', 'body', 'created', 'comments']
        extra_fields = []
