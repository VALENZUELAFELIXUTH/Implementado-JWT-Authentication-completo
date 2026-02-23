# biblioteca_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 2. Endpoints de la API (Aquí es donde usas Postman o Curl)
    path('api/', include('libros.api_urls')),
    
    
]