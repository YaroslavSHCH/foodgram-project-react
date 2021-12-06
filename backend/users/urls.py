from django.urls import re_path, path, include
from rest_framework import routers

from .views import UserViewSet, SubscriptionViewSet, UpdatePasswordAPIView, add_subscription

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('users/set_password/', UpdatePasswordAPIView.as_view()),
    path('users/subscriptions/', SubscriptionViewSet.as_view({'get': 'list'})),
    re_path(r'users/(?P<user_id>[0-9]+)/subscribe/', add_subscription),
    path('', include(router.urls)),
]
