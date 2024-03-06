
from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/',views.api_home),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/images/',views.ImageListCreateAPIView.as_view(),name='image-list'),
    path('api/images/<int:pk>/delete/',views.ImageDestroyAPIView.as_view(),name='image-delete'),
    path('api/images/<int:pk>/update/',views.ImageUpdateAPIView.as_view(),name='image-update'),
    path('api/users/',views.UserListCreateAPIView.as_view(),name='user-search'),
    path('api/users/<int:pk>/delete/',views.UserDestroyAPIView.as_view(),name='user-delete'),
]