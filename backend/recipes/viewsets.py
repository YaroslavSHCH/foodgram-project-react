from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin, RetrieveModelMixin,
                                   UpdateModelMixin)
from rest_framework.viewsets import GenericViewSet


class ModelCUVDViewSet(CreateModelMixin,
                       DestroyModelMixin,
                       ListModelMixin,
                       UpdateModelMixin,
                       RetrieveModelMixin,
                       GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`,
    `destroy()` and `list()` actions for RecipesApp.
    """
    pass
