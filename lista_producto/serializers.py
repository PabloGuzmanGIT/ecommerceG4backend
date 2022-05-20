from rest_framework import serializers
from .models import Muebles,ListaProducto, Picture
from fac_electronica.models import Pedido

class MueblesSerializer(serializers.ModelSerializer):
    class Meta:
        fields='__all__'
        model=Muebles        
 
class MuebleSerializer(serializers.ModelSerializer):
    class Meta:
        fields='categoria'
        model=Muebles
        depth=1

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


class BuscarMueblesSerializer(serializers.Serializer):
    categoria=serializers.CharField()

class AgregarListadoProductosSerializer(serializers.Serializer):
    fecha = serializers.DateTimeField()
    cantidad = serializers.IntegerField(min_value=1)
    precio_diario = serializers.IntegerField(min_value=1)
    muebleId = serializers.IntegerField(min_value=1)

class ListaProductosSerializer(serializers.ModelSerializer):
    class Meta:
        fields='__all__'
        model=ListaProducto

class ArchivoSerializer(serializers.Serializer):
    # max_length > indica la longitud maxima DEL NOMBRE del archivo
    # use_url > si es verdadero retornara el link completo de la ubicacion del archivo, caso contrario retornara solamente la ubicacion dentro del proyecto del archivo

    archivo = serializers.ImageField(max_length=100, use_url=True)

class EliminarArchivoSerializer(serializers.Serializer):
    archivo = serializers.CharField(max_length=100)

class PruebaDisponibleSerializer(serializers.ModelSerializer):
    class Meta:
        fields='__all__'
        model=Muebles  

class ArchivoPictureSerializer(serializers.ModelSerializer):

    class Meta:
        fields='__all__'
        model=Picture     