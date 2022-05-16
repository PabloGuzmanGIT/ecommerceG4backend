from django.urls import path
from .views import (
                        MueblesApiView,
                        MuebleApiView,
                        ListaProductoApiView,
                        PedidoApiView,
                        AgregarDetallePedidoApiView,
                        AgregarListadoProductosApiView,                                                                
                        BuscarCategoriaProductosApiView,
                        BuscarProductosDisponiblesApiView                                       
                    )

urlpatterns = [
    path('', MueblesApiView.as_view()),
    path('<int:pk>/', MuebleApiView.as_view()), 
    path('lista-producto/', ListaProductoApiView.as_view()),
    path('pedido/', PedidoApiView.as_view()),
    path('agregar-detalle/', AgregarDetallePedidoApiView.as_view()),  
    path('lista_productos/', AgregarListadoProductosApiView.as_view()),
    path('buscar-categoriaProductos/',BuscarCategoriaProductosApiView.as_view()),
    path('buscar-disponible/', BuscarProductosDisponiblesApiView.as_view())
]