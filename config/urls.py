from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from catalog.auth_views import register_view
 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/register/', register_view, name='register'),
    path('api/auth/login/',    TokenObtainPairView.as_view(), name='login'),
    path('api/auth/refresh/',  TokenRefreshView.as_view(),    name='refresh'),
    path('api/', include('catalog.urls')),
]
