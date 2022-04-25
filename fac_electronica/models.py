from xmlrpc.client import DateTime
from django.db import models
from autorizacion.models import Usuario
from lista_producto.models import ListaProducto
from django.utils import timezone

class Pedido(models.Model):    
    id=models.AutoField(primary_key=True)        
    fecha=models.DateTimeField(default=timezone.now)
    total=models.FloatField(null=False)
    numeroDocumentoCliente=models.CharField(max_length=12,null=True)
    tipoDocumentoCliente=models.CharField(choices=(['RUC','RUC'],['DNI','DNI']),max_length=5,null=True)
    mesa=models.IntegerField(null=False)
    propina=models.IntegerField()

    # comprobante=models.OneToOneField(
    #     to=Usuario,related_name='pedidos',on_delete=models.CASCADE, db_column='usuario_id' 
    # )

    usuarioId=models.ForeignKey(to=Usuario,related_name="pedidos",on_delete=models.CASCADE,db_column='usuario_id')

    class Meta:
        db_table='pedidos'
   
class DetallePedido(models.Model):    
    id=models.AutoField(primary_key=True,null=False)    
    cantidad=models.IntegerField()    
    listaProductoId=models.ForeignKey(to=ListaProducto,related_name="detalle_pedidos",on_delete=models.CASCADE,db_column='lista_producto_id')
    pedidoId=models.ForeignKey(to=Pedido,related_name="detalle_pedidos",on_delete=models.CASCADE,db_column='pedido_id')

    class Meta:
        db_table='detalle_pedidos'
   
class Comprobante(models.Model):
    id=models.AutoField(primary_key=True)    
    serie=models.CharField(max_length=5,null=False)
    numero=models.CharField(max_length=5,null=False)
    pdf=models.TextField()
    cdr=models.TextField()
    xml=models.TextField()
    tipo=models.CharField(max_length=10,choices=(['BOLETA','BOLETA'],['FACTURA','FACTURA']),null=False)
    pedido=models.OneToOneField(
        to=Pedido,related_name='comprobante',on_delete=models.CASCADE,db_column='pedido_id'
    )
    class Meta:
        db_table='comprobantes'
        unique_together=[['serie','numero']]
