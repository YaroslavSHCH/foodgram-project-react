from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .pagination import CustomResultsPagination
from .models import Follow, User
from .viewsets import ModelCVViewSet
from .serializers import (ChangePasswordSerializer,
                          UserSerializer,
                          SubscribeSerializer)


class UserViewSet(ModelCVViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomResultsPagination

    def retrieve(self, request, *args, **kwargs):
        """"Method with url kwargs handler."""
        if kwargs.get('pk') == 'me':
            user = User.objects.get(id=request.user.id)
        else:
            user = User.objects.get(id=kwargs.get('pk'))
        serializer = self.get_serializer(user)
        return Response(serializer.data)


class SubscriptionViewSet(ModelViewSet):
    serializer_class = SubscribeSerializer
    pagination_class = CustomResultsPagination

    def get_queryset(self):
        user = self.request.user
        follows = Follow.objects.filter(
            user=user
        ).select_related(
            'following'
        ).values_list(
            'following_id', flat=True
        )
        users = User.objects.filter(id__in=follows)
        return users


@api_view(['GET', 'DELETE'])
def add_subscription(request, **kwargs):
    if request.method == 'GET':
        user = request.user
        following = get_object_or_404(User, id=kwargs['user_id'])
        if Follow.objects.get_or_create(user=user, following=following)[1]:
            return Response(SubscribeSerializer(
                following, context={'request': request}).data)

        return Response({'error': 'Вы уже подписаны на данного пользователя'},
                        status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        user = request.user
        subscribe = get_object_or_404(
            Follow, following_id=kwargs['user_id'], user=user)
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response({'error': 'Не допустимый тип запроса'})


class UpdatePasswordAPIView(APIView):
    """An endpoint for changing password."""
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("current_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
