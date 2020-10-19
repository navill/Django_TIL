# # Create your views here.
# from rest_framework import status
# from rest_framework.generics import GenericAPIView
# from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
#
# from blog.models import Post, Comment
# from blog.serializers import PostSerializer, CommentSerializer
#
#
# class PostView(ListModelMixin, CreateModelMixin, RetrieveModelMixin, GenericAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [AllowAny]
#
#     def get(self, request, *args, **kwargs):
#         if kwargs.get('pk', None):
#             response = self.retrieve(request, *args, **kwargs)
#         else:
#             response = self.list(request, *args, **kwargs)
#         return response
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#     def retrieve(self, request, *args, **kwargs):
#         # instance = self.get_object()
#         instance = Post.objects.prefetch_related('comments').get(id=kwargs['pk'])
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
#     def list(self, request, *args, **kwargs):
#         # queryset = self.filter_queryset(self.get_queryset())  # query: 8
#         # queryset = Post.objects.prefetch_related('comments')
#         queryset = Post.objects.prefetch_related('comments')  # query: 5
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)
#
#
# class CommentView(CreateModelMixin, ListModelMixin, RetrieveModelMixin, GenericAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     permission_classes = [AllowAny]
#
#     def get(self, request, *args, **kwargs):
#         if kwargs.get('pk', None):
#             response = self.retrieve(request, *args, **kwargs)
#         else:
#             response = self.list(request, *args, **kwargs)
#         return response
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data)
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
#     def list(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#
#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)
# views
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse


@permission_required('blog.close_task', login_url='/admin/login/')
def test_view(request):
    return HttpResponse('accept')



