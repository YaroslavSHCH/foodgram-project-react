from django.urls import path, include
from rest_framework import routers

from .views import UserViewSet, SubscriptionViewSet, UpdatePasswordAPIView

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('users/set_password/', UpdatePasswordAPIView.as_view()),
    path('users/subscriptions/', SubscriptionViewSet.as_view({'get': 'list'})),
    path('', include(router.urls)),
]
