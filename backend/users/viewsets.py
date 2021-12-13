from rest_framework.mixins import (CreateModelMixin, ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.viewsets import GenericViewSet


class ModelCVViewSet(CreateModelMixin,
                     ListModelMixin,
                     RetrieveModelMixin,
                     GenericViewSet):
    """
    A viewset that provides default `create()`, `retrieve()`,
    `destroy()` and `list()` actions for UsersApp.
    """
    pass
