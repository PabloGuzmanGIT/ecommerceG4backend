from .models import Muebles,ListaProducto
from rest_framework.generics import ListCreateAPIView,CreateAPIView,ListAPIView,RetrieveAPIView
from .serializers import ( 
                            MueblesSerializer,
                            MuebleSerializer,                        
                            PedidoSerializer,
                            AgregarDetallePedidoSerializer,
                            ListaProductoSerializer,
                            ListaProductoCreateSerializer,
                            AgregarListadoProductosSerializer,
                            ListaProductosSerializer                                                 
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
from django.shortcuts import get_list_or_404, get_object_or_404

class MueblesApiView(ListCreateAPIView):
    queryset=Muebles.objects.all()
    serializer_class=MueblesSerializer
    permission_classes=[IsAuthenticatedOrReadOnly,SoloAdminPuedeEscribir]

    def post(self,request: Request):
        #print(request.user)
        request.data['usuarioId']=request.user.id
        data=self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        data.save()
        return Response(data=data.data,status=status.HTTP_201_CREATED) 

    def get(self, request: Request):
        #queryset=Mueble.objects.all()
        data = self.serializer_class(instance=self.get_queryset(), many=True)   
        return Response(data=data.data)

class MuebleApiView(ListAPIView):   
    queryset=Muebles.objects.all()
    serializer_class=MuebleSerializer
    permission_classes=[IsAuthenticatedOrReadOnly,SoloAdminPuedeEscribir]

    def get(self, request: Request):                 
        #request.data['categoria']=request.mueble.categoria        
        data = self.serializer_class.filter(categoria=request.categoria)
        return Response(data=data.data)
        #return Response(data=serializer_class.data)
 
class ListaProductoApiView(ListCreateAPIView):
    # serializer_class=StockSerializer
    queryset=ListaProducto.objects.all()
    permission_classes=[IsAuthenticatedOrReadOnly,SoloAdminPuedeEscribir]
    # permission_classes=[IsAuthenticatedOrReadOnly]

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
        listaProducto : ListaProducto | None = ListaProducto.objects.filter(fecha=timezone.now(),muebleId=data.validated_data.get('muebleId'),cantidad__gte=data.validated_data.get('cantidad')).first()
        print(listaProducto)
        #agrego el detalle data=self.serializer_class(data=request.data)
        if listaProducto is None:                
            #agregar aqui el print de foto en no disponible TAREA DEL PROFESOR
            return Response(data={'message':'No hay stock de este mueble para el día de hoy'},status=status.HTTP_400_BAD_REQUEST)
            
        #validar si el pedido existe        
        pedido: Pedido | None = Pedido.objects.filter(id=data.validated_data.get('pedidoId')).first()
        if pedido is None: 
            return Response(data={'message':'No existe ese código de pedido'},status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                nuevoDetalle=DetallePedido(cantidad=data.validated_data.get('cantidad'),listaProductoId=listaProducto,pedidoId=pedido)
                nuevoDetalle.save()
                #disminuir el stock del mueble pedido
                listaProducto.cantidad=listaProducto.cantidad-nuevoDetalle.cantidad
                #guardar ese detalle de ese pedido
                listaProducto.save()
                # modifico el total de la cacbecera
                pedido.total=pedido.total + (nuevoDetalle.cantidad * listaProducto.precio_diario)
                pedido.save()
                #si el bloque termina todo bien automaticamente ejecuta un commit a la db
        except IntegrityError:
            #aqui ingresa si algo no funciona de la manera esperada
            #rollback
            return Response(data={'message':'Error al crear el pedido'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data={'message':'Detalle creado exitosamente'},status=status.HTTP_201_CREATED)  


class BuscarProductosApiView(ListCreateAPIView):    
    serializer_class = MueblesSerializer    
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Muebles.objects.all()
   
    def get(self, request: Request):
        categoria = self.request.query_params.get('categoria', None)          
        queryset = Muebles.objects.filter(categoria=categoria).all()  
        data = self.serializer_class(instance=queryset, many=True)     
                
        if len(data.data) == 0:
            return Response(data={"message":"No existe esa categoria de muebles"})        

        return Response(data=data.data)

class PedidosApiView(ListCreateAPIView):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated, SoloClientePuedeEscribir]

    def post(self, request: Request):
        print(request.user)
        request.data['usuarioId'] = request.user.id
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        data.save()
        return Response(data=data.data, status=status.HTTP_201_CREATED)

class AgregarListadoProductosApiView(CreateAPIView):
    queryset = ListaProducto.objects.all()
    serializer_class = AgregarListadoProductosSerializer
    permission_classes = [IsAuthenticated, SoloAdminPuedeEscribir]

    def post(self, request: Request):
        print(request.data)       
        data = self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)

        producto: Muebles | None = Muebles.objects.filter(id=data.validated_data.get('muebleId')).first()
      
        if producto is None:
            return Response(data={'message': 'Código de mueble no existe'}, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     if producto.disponible == False:
        #         return Response(data={'message': 'Mueble no disponible'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:           
            ListadoProducto = ListaProducto(fecha=timezone.now(),precio_diario=data.validated_data.get('precio_diario'),
                             cantidad=data.validated_data.get('cantidad'), muebleId=producto)
            print(ListadoProducto)
            ListadoProducto.save()

        except Exception as e:
            return Response(data={'message': 'Error no se pudo crear el registro',
                                  'content': e.args},status=status.HTTP_400_BAD_REQUEST)

        
        return Response(data=data.data)

class BuscarCategoriaProductosApiView(ListAPIView):
    queryset = Muebles.objects.all()
    serializer_class = MueblesSerializer
    permission_classes = [IsAuthenticated,SoloClientePuedeEscribir]

    def get(self, request: Request):
        categoria = self.request.query_params.get('categoria',None)

        mueble: Muebles | None = Muebles.objects.filter(categoria=categoria).first()

        if mueble is None:
            return Response(data={'message':'Categoria no existe'})
       
        listaqs= mueble.lista_productos.all()              
        data = ListaProductosSerializer(instance=listaqs, many=True)

        if len(data.data)==0:
            return Response(data={'message':'No hay productos para mostrar'})
       
        return Response(data.data)

class BuscarProductosDisponiblesApiView(ListAPIView):
    serializer_class = ListaProductosSerializer    
    queryset = ListaProducto.objects.all()
    permission_classes = [IsAuthenticated,SoloClientePuedeEscribir]
     
    def get(self, request:Request):
        listadoProductoId = self.request.query_params.get('id', None)

        listaProducto: ListaProducto | None = ListaProducto.objects.filter(id=listadoProductoId).first()

        if listaProducto is None:
            return Response(data={'message':'Código de stock de mueble no existe'})
        
        mueble: Muebles | None = Muebles.objects.filter(id=listaProducto.muebleId.id).first()
             
        if mueble.disponible == False:
            return Response(data={'message':'Mueble no disponible'},status=status.HTTP_404_NOT_FOUND)
        else:
            data = self.serializer_class(instance=listaProducto)        
            return Response(data.data)

    
    
  

            