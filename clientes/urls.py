from django.urls import path
from .views import lista_clientes, ver_entrega_cliente
from django.contrib.staticfiles.urls import static 

from django.conf import settings

urlpatterns = [
    path('estado/', lista_clientes, name='lista_clientes'),
    path('entrega/<str:placa>/',ver_entrega_cliente,name='ver_entrega_cliente'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)