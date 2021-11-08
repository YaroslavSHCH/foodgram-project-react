from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('recipe/', include('recipes.urls')),
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')), 
]
