from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def home(request):
    return HttpResponse("🔥 Planta Digital funcionando!")

urlpatterns = [
    path('admin/', admin.site.urls),

    # 👇 esto mantiene tus rutas reales
    path('', include('core.urls')),

    # 👇 opcional fallback si core no tiene home
    path('test/', home),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)