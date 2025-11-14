from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # URL para acessar o admin do Django
    path('', include('core.urls')),   # Incluir as URLs da aplicação 'core'
]

# Adicionando as configs para servir arquivos de mídia
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
