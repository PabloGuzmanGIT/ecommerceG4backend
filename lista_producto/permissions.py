from rest_framework.permissions import BasePermission,SAFE_METHODS
from rest_framework.request import Request

class SoloAdminPuedeEscribir(BasePermission):
    message='Este usuario no tiene permisos'
    def has_permission(self,request,view):

        #request nos dara toda la info de atributos de la peticion                
        print(request.user)
        print(request.user.nombre)
        print(request.user.rol)

        #imprime la token de autenticacion
        print(request.auth)
        print(request.method)
        print(SAFE_METHODS)
        print(type(view))

       #si es GET,HEAD,OPTIONS no necsita validar si es ADMINISTRADOR o MOZO
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.rol=='ADMINISTRADOR'
        
        return True if request.method in SAFE_METHODS else request.user.rol=='ADMINISTRADOR'
        
class SoloClientePuedeEscribir(BasePermission):
    
    message='Este usuario no tiene permisos'
    def has_permission(self,request,view):
        return True if request.method in SAFE_METHODS else request.user.rol=='CLIENTE'