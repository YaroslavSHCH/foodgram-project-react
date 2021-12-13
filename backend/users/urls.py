from django.urls import path

from .views import SubscriptionViewSet, UpdatePasswordAPIView

urlpatterns = [
    path(
        'users/set_password/',
        UpdatePasswordAPIView.as_view(),
        name='set_password'
    ),
    path(
        'users/subscriptions/',
        SubscriptionViewSet.as_view({'get': 'list'}),
        name='subscriptions'
    )
]
