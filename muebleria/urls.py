from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/',include('autorizacion.urls')),
    path('muebles/', include('lista_producto.urls')),
    path('facturacion/', include('fac_electronica.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
