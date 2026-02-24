# biblioteca_project/urls.py

from django.contrib import admin
from django.urls import path, include
from libros.jwt_views import CustomTokenObtainPairView, get_user_tokens
from libros import web_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 2. Endpoints de la API (Aquí es donde usas Postman o Curl)
    path('api/', include('libros.api_urls')),
    # JWT personalizado
    path('auth/jwt/login/', CustomTokenObtainPairView.as_view(), name='jwt_login'),
    
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    path('accounts/', include('allauth.urls')),
    path('api/get-tokens/', get_user_tokens, name='get_tokens'),

    path('', web_views.home, name='home'),
    path('oauth/login/', web_views.oauth_login, name='oauth_login'),
    path('login/jwt/', web_views.jwt_login_page, name='jwt_login_page'),
]