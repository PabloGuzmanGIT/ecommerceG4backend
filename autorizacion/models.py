from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .authManager import UserManager
#el AbstractBaseUser permite trabajar con toda la tabla desde cero

class Usuario(AbstractBaseUser, PermissionsMixin):
    id=models.AutoField(primary_key=True)
    nombre=models.CharField(max_length=45,null=False)
    apellidos=models.CharField(max_length=90,unique=True,null=False)
    correo=models.EmailField(unique=True,null=False)
    telefono=models.IntegerField(null=False)
    usuario=models.CharField(max_length=45,unique=True,null=False)
    password=models.TextField(null=False)
    rol=models.CharField(
        choices=(['ADMINISTRADOR','ADMINISTRADOR'],['CLIENTE','CLIENTE']),max_length=40
    )
    #algunas columnas para el panel administrativo postgres
    #is_Staff: autoriza segu  usuario
    is_staff=models.BooleanField(default=False)
    #is_active: si puede hacer cambios en panel admin
    is_active=models.BooleanField(default=True)
    createdAt=models.DateTimeField(auto_now_add=True,db_column='created_at')
    #comportaminto que tendra el modelo cuando se realice el createsuperuser
    objects=UserManager()    
    USERNAME_FIELD='correo'
    #input requeridos (no se colocan los passsword, o unique) es obvio:: correo,usuario
    REQUIRED_FIELDS=['nombre','apellidos','telefono','rol']
    class Meta:
        db_table='usuarios'