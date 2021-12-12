from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from rest_framework import routers

import authentication.urls

from recipes.views import RecipeViewSet, TagViewSet, IngredientViewSet
from users.views import UserViewSet, SubscriptionViewSet, UpdatePasswordAPIView

router = routers.DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/set_password/', UpdatePasswordAPIView.as_view()),
    path(
        'api/users/subscriptions/',
        SubscriptionViewSet.as_view({'get': 'list'})
    ),
    path('api/', include(router.urls)),
    path('api/', include(authentication.urls)),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
