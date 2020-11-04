from django.contrib.auth import get_user_model
from rest_framework import serializers

from blog.models import MyModel

User = get_user_model()


# class CommentSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#     post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())
#     comment = serializers.CharField()
#
#     class Meta:
#         model = Comment
#         fields = '__all__'
#
#
# class PostSerializer(serializers.ModelSerializer):
#     user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
#     title = serializers.CharField()
#     body = serializers.CharField()
#     comments = serializers.StringRelatedField(many=True)
#
#
#     class Meta:
#         model = Post
#         fields = ['user', 'title', 'body', 'created', 'comments']
#         extra_fields = []


class MySerializer(serializers.ModelSerializer):
    multi_value = serializers.SerializerMethodField()

    def get_multi_value(self, obj):
        return obj.value * 1000

    def to_representation(self, instance):
        value = self.fields['multi_value']
        multi_value = value.to_representation(
            value.get_attribute(instance))
        return {
            'name': instance.title,
            'value * 1000': multi_value
        }

    class Meta:
        model = MyModel
        fields = ['title', 'value', 'multi_value']

