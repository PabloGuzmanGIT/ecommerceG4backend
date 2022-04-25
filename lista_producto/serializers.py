from rest_framework import serializers
from .models import Mueble,ListaProducto
from fac_electronica.models import Pedido

class MuebleSerializer(serializers.ModelSerializer):
    class Meta:
        fields='__all__'
        model=Mueble


class ListaProductoSerializer(serializers.ModelSerializer):
    class Meta:
        fields='__all__'
        model=ListaProducto
        depth=1

class ListaProductoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        fields='__all__'
        model=ListaProducto

class PedidoSerializer(serializers.ModelSerializer):
    class Meta:
        fields='__all__'
        model=Pedido

class AgregarDetallePedidoSerializer(serializers.Serializer):
    cantidad=serializers.IntegerField(min_value=1)
    pedidoId = serializers.IntegerField(min_value=1)
    muebleId=serializers.IntegerField(min_value=1)