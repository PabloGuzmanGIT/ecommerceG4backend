from rest_framework import serializers
from .models import Usuario

class RegistroUsuarioSeriaizer(serializers.ModelSerializer):
    def save(self):        
        #crearemos una instancia de mi usuario con campos ya validados
        nuevoUsuario=Usuario(**self.validated_data)
        #encripto la contraseña
        nuevoUsuario.set_password(self.validated_data.get('password'))
        nuevoUsuario.save()
        return nuevoUsuario    
    
    class Meta:
        model=Usuario
        fields='__all__'
        #exclude=['groups','user_permissions']
        # mediante el atribuo extra_kwargs indicar pass solo escritura
        extra_kwargs={
            'password':{'write_only':True},            
            'id':{'read_only':True},
        }
        