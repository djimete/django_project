from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Interface admin
    path('admin/', admin.site.urls),

    # Toutes les URLs de ton application principale
    path('', include('myApp.urls')),
]

# Gestion des fichiers médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
