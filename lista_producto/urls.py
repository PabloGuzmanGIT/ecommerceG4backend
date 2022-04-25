from django.urls import path
from .views import (
                        MuebleApiView,
                        ListaProductoApiView,
                        PedidoApiView,
                        AgregarDetallePedidoApiView
                    )

urlpatterns = [
    path('', MuebleApiView.as_view()),
    path('lista-producto/', ListaProductoApiView.as_view()),
     path('pedido/', PedidoApiView.as_view()),
     path('agregar-detalle/', AgregarDetallePedidoApiView.as_view()),
]