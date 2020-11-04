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
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView, DetailView, ListView, TemplateView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from blog.forms import FlavorForm
from blog.models import Flavor, IceCreamStore, Voucher, MyModel
from blog.serializers import MySerializer


@permission_required('blog.close_task', login_url='/admin/login/')
def test_view(request):
    return HttpResponse('accept')


# ----------------------------------------------------------------------------------------------------
class FlavorActionMixin:
    model = Flavor
    fields = ['title', 'slug', 'scoops_remaining']

    @property
    def success_msg(self):
        return NotImplemented

    def form_valid(self, form):
        messages.info(self.request, self.success_msg)
        super().form_valid(form)


class FlavorCreateView(LoginRequiredMixin, FlavorActionMixin, CreateView):
    success_msg = 'created'
    form_class = FlavorForm


class FlavorUpdateView(LoginRequiredMixin, FlavorActionMixin, UpdateView):
    success_msg = 'updated'
    form_class = FlavorForm


class FlavorDetailView(DetailView):
    model = Flavor


class TitleSearchMixin:
    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get('q')
        if q:
            return queryset.filter(title__icontains=q)
        return queryset


class FlavorListView(TitleSearchMixin, ListView):
    model = Flavor


class IceCreamListVIew(TitleSearchMixin, ListView):
    model = IceCreamStore


# ----------------------------------------------------------------------------------------------------

class GreenfeldRoyView(TemplateView):
    template_name = 'vouchers/views_conditional.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['greenfields'] = Voucher.objects.filter(name__icontains='greenfeld')
        context['roys'] = Voucher.objects.filter(name__icontains='roy')
        return context


# ----------------------------------------------------------------------------------------------------
class MyModelView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = MyModel
    serializer_class = MySerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
