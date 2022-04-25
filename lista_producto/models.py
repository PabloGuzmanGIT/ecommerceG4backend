from django.db import models
from cloudinary import models as modelsCloudinary

class Mueble(models.Model):   #tabla referencia platos 
    id=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=45,unique=True,null=False)
    precio=models.FloatField(null=False)
     #foto=models.ImageField(upload_to='multimedia',null=True)
    foto1=modelsCloudinary.CloudinaryField( folder='muebles')
    foto2=modelsCloudinary.CloudinaryField( folder='muebles')
    foto3=modelsCloudinary.CloudinaryField( folder='muebles')
    disponible=models.BooleanField(default=True,null=False)
        
    class Meta:
        db_table='muebles'

class ListaProducto(models.Model): #tabla referencia menus
    id=models.AutoField(primary_key=True)
    fecha=models.DateField(null=False)         
    cantidad=models.IntegerField(null=False)
    precio_diario=models.FloatField(null=False)    
    muebleId=models.ForeignKey(to=Mueble,related_name="lista_productos",on_delete=models.CASCADE,db_column='lista_producto_id')
    class Meta:
        db_table='lista_productos'
        #unique-together: crea un indice de dos o mas columnas :: foregin key
        unique_together=[['fecha','muebleId']]
