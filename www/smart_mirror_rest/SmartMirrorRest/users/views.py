from django.shortcuts import render
from rest_framework import generics
from rest_framework import mixins
from django.views.decorators.csrf import csrf_exempt

from .models import Users
from .serializers import UsersSerializer

# Create your views here.

class UsersListAPI(generics.GenericAPIView, mixins.CreateModelMixin, mixins.ListModelMixin):
    serializer_class = UsersSerializer 

    def get_queryset(self): 
        return Users.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class UsersDetailAPI(generics.GenericAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.RetrieveModelMixin):
    serializer_class = UsersSerializer

    def get_queryset(self):
        return Users.objects.all().order_by('id')

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    # put은 update을 내보내는 메소드
    @csrf_exempt
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @csrf_exempt
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    # delete은 destroy를 내보내는 메소드
    @csrf_exempt
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)