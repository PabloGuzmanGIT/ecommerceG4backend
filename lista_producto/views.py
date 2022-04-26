from .models import Mueble,ListaProducto
from rest_framework.generics import ListCreateAPIView,CreateAPIView
from .serializers import (  MuebleSerializer,
                            ListaProductoSerializer,
                            PedidoSerializer,
                            AgregarDetallePedidoSerializer,
                            ListaProductoCreateSerializer
                        )
from rest_framework.permissions import (# sirve para que el controlador sea publico (no se necesite una token)
                                        AllowAny,  
                                        # Los controladores soliciten una token de acceso
                                        IsAuthenticated,
                                        # Solamente para los metodos GET no sera necesaria la token pero para los demas metodos (POST, PUT, DELETE, PATCH) si sera requerido
                                        IsAuthenticatedOrReadOnly,
                                        # Verifica que en la token de acceso buscara al usuario y vera si es superuser (is_superuser)
                                        IsAdminUser,
                                        SAFE_METHODS
                                        )
from rest_framework.response import Response
from rest_framework.request import Request
from cloudinary import CloudinaryImage
from .permissions import SoloAdminPuedeEscribir,SoloClientePuedeEscribir
from fac_electronica.models import Pedido,DetallePedido
from rest_framework import status
from django.utils import timezone
from django.db import transaction,IntegrityError

class MuebleApiView(ListCreateAPIView):
    serializer_class = MuebleSerializer
    queryset = Mueble.objects.all()
    # sirve para indicar que tipos de permisos necesita el cliente para poder realizar la peticion
    permission_classes = [IsAuthenticatedOrReadOnly]


#CONSULTAR AL PROFESOR COMO SELECCIONAR 3 FOTOS
    def get(self, request: Request):
        data = self.serializer_class(instance=self.get_queryset(), many=True)       
        print(data.data[1].get('foto1'))
        print(data.data[1].get('foto2'))
        print(data.data[1].get('foto3'))
        return Response(data=data.data)
class ListaProductoApiView(ListCreateAPIView):
    # serializer_class=StockSerializer
    queryset=ListaProducto.objects.all()
    permission_classes=[IsAuthenticatedOrReadOnly,SoloAdminPuedeEscribir]

    def get_serializer_class(self):
        if not self.request.method in SAFE_METHODS:
            return ListaProductoCreateSerializer
        return ListaProductoSerializer

class PedidoApiView(ListCreateAPIView):
    queryset=ListaProducto.objects.all()
    serializer_class=PedidoSerializer
    permission_classes=[IsAuthenticatedOrReadOnly,SoloClientePuedeEscribir]
    def post(self,request: Request):
        print(request.user)
        request.data['usuarioId']=request.user.id
        data=self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        data.save()
        return Response(data=data.data,status=status.HTTP_201_CREATED)

class AgregarDetallePedidoApiView(CreateAPIView):
    queryset=DetallePedido.objects.all()
    serializer_class=AgregarDetallePedidoSerializer
    permission_classes=[IsAuthenticated,SoloClientePuedeEscribir]
    def post(self,request: Request):
        #valido la data        
        data=self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)

        #verifico que tenga cantidad de muebles en stock
        stock : ListaProducto | None = ListaProducto.objects.filter(fecha=timezone.now(),muebleId=data.validated_data.get('muebleId'),cantidad__gte=data.validated_data.get('cantidad')).first()
        print(stock)
        #agrego el detalle data=self.serializer_class(data=request.data)
        if stock is None:                
            #agregar aqui el print de foto en no disponible TAREA DEL PROFESOR
            return Response(data={'message':'No hay stock para este producto'},status=status.HTTP_400_BAD_REQUEST)
            
        #validar si el pedido existe        
        pedido: Pedido | None = Pedido.objects.filter(id=data.validated_data.get('pedidoId')).first()
        if pedido is None: 
            return Response(data={'message':'No hay ese pedido'},status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                nuevoDetalle=DetallePedido(cantidad=data.validated_data.get('cantidad'),stockId=stock,pedidoId=pedido)
                nuevoDetalle.save()
                #disminuir el stock del mueble pedido
                stock.cantidad=stock.cantidad-nuevoDetalle.cantidad
                #guardar ese detalle de ese pedido
                stock.save()
                # modifico el total de la cacbecera
                pedido.total=pedido.total + (nuevoDetalle.cantidad * stock.precio_diario)
                pedido.save()
                #si el bloque termina todo bien automaticamente ejecuta un commit a la db
        except IntegrityError:
            #aqui ingresa si algo no funciona de la manera esperada
            #rollback
            return Response(data={'message':'Error al crear el pedido'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data={'message':'Detalle creado exitosamente'},status=status.HTTP_201_CREATED)