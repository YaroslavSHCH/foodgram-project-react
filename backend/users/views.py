from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Follow, User
from .pagination import CustomResultsPagination
from .serializers import (ChangePasswordSerializer, SubscribeSerializer,
                          UserSerializer)
from .viewsets import ModelCVViewSet


class UserViewSet(ModelCVViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomResultsPagination

    @action(methods=['get'],
            detail=False,
            permission_classes=[IsAuthenticated])
    def me(self, request, pk=None):
        user = self.request.user
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get', 'delete'],
            detail=True,
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, pk=None):
        user = self.request.user
        following = self.get_object()
        if request.method == 'GET':
            subscribe = Follow.objects.get_or_create(
                user=user,
                following=following)
            if not subscribe[1]:
                return Response(
                    {'detail': 'Вы уже подписаны на этого пользователя'},
                    status.HTTP_400_BAD_REQUEST)

            serializer = SubscribeSerializer(
                following,
                context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            subscribe = get_object_or_404(
                Follow,
                user=user,
                following=following
            )
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=['get'],
        detail=False,
        serializer_class=SubscribeSerializer,
        permission_classes=[IsAuthenticated],
        pagination_class=CustomResultsPagination
    )
    def subscriptions(self, request, *args, **kwargs):
        user = request.user
        queryset = User.objects.filter(followings__user=user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = SubscribeSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = SubscribeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdatePasswordAPIView(APIView):
    """An endpoint for changing password."""
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        old_password = serializer.validated_data.get('current_password')
        if not self.object.check_password(old_password):
            return Response({'current_password': 'Неверный пароль'},
                            status=status.HTTP_400_BAD_REQUEST)
        self.object.set_password(serializer.validated_data.get('new_password'))
        self.object.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
