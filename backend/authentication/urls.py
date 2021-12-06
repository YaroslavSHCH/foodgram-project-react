from django.urls import path

from .views import CustomAuthToken, LogoutAPIView

urlpatterns = [
    path('auth/token/login/', CustomAuthToken.as_view(), name='user_login'),
    path('auth/token/logout/', LogoutAPIView.as_view(), name='user_logout')
]
