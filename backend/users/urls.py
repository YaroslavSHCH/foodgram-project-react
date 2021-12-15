from django.urls import path

from .views import UpdatePasswordAPIView

urlpatterns = [
    path(
        'users/set_password/',
        UpdatePasswordAPIView.as_view(),
        name='set_password'
    )
]
