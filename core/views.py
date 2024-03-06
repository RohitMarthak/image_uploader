from . serializers import ImageSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

from .models import User,Image
from .serializers import UserSerializer,ImageSerializer

from rest_framework.permissions import IsAuthenticated
from .permissions import IsSuperUserOrOwner

from rest_framework.pagination import LimitOffsetPagination

@api_view(['POST'])
def api_home(request, *args, **kwargs):
 
    serializer =ImageSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
       
        print(serializer.data)
        return Response(serializer.data)
    return Response({"invalid": "not good data"}, status=400)


class ImageListCreateAPIView(generics.ListCreateAPIView,):

    images = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated,IsSuperUserOrOwner]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Image.objects.all()
        else:
            return Image.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ImageDestroyAPIView(generics.DestroyAPIView):

    queryset = Image.objects.all()
    lookup_field = 'pk'
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated,IsSuperUserOrOwner]

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)

class ImageUpdateAPIView(generics.UpdateAPIView):

    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated,IsSuperUserOrOwner]
    lookup_field = 'pk'

    def perform_update(self, instance):
        return super().perform_update(instance)


class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class=LimitOffsetPagination

    def get_queryset(self):
        request = self.request
        q = request.GET.get('q')

        results = User.objects.all()

        if q is not None:
            results = User.objects.filter(username__icontains=q)

        return results

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True, is_staff=True)
        user.set_password(serializer.validated_data['password'])
        user.save()

class UserDestroyAPIView(generics.DestroyAPIView):

    queryset = User.objects.all()
    lookup_field = 'pk'
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,IsSuperUserOrOwner]

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)

