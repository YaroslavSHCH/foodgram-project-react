from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from django.contrib import admin
from rest_framework import routers

import shoppingcart.urls
import users.urls
import authentication.urls

from recipes.views import RecipeViewSet, TagViewSet, IngredientViewSet

router = routers.DefaultRouter()
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredient')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(users.urls)),
    path('api/', include(router.urls)),
    path('api/', include(authentication.urls)),
    path('api/recipes/', include(shoppingcart.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
