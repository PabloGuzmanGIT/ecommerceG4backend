from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    """Clase que sirve para manejar el comportamiento del auth_user"""
    def create_user(self, nombre,apellidos,correo,telefono,usuario,password,rol):
        """Creacion de un usuario sin el comando createsuperuser"""
        if not correo:
            raise ValueError("El user debe completar los campos requeridos")
        #normalizando
        nombre=self(nombre)
        apellidos=self(apellidos)
        correo=self.normalize_email(correo)
        telefono=self(telefono)
        usuario=self(usuario)
        #manda a llamar al modelo usuario e iniciara su construccion
        nuevoUsuario=self.model(nombre=nombre,apellidos=apellidos,correo=correo,telefono=telefono,usuario=usuario,rol=rol)        
        nuevoUsuario.set_password(password)
        #sirve para direccionar la conexion a la db
        nuevoUsuario.save(using=self._db)
        return nuevoUsuario
    
    """Creacion de un sa por consola"""
    def create_superuser(self, nombre,apellidos,correo,telefono,usuario,password,rol):
        usuario=self.create_user(nombre,apellidos,correo,telefono,usuario,password,rol)
        usuario.is_superuser=True
        usuario.is_staff=True
        usuario.save(using=self._db)