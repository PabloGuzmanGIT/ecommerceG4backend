from rest_framework.generics import CreateAPIView
from rest_framework.request import Request
from .serializers import RegistroUsuarioSeriaizer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.utils import timezone
from os import remove
from django.conf import settings

# @api_view(http_method_names=['GET', 'POST'])
# def inicio(request: Request):
#     # request sera toda la informacion enviada por el cliente > https://www.django-rest-framework.org/api-guide/requests/
#     print(request.method)
#     print(request)
#     if request.method == 'GET':
#         return Response(data={
#             'message': 'Bienvenido a mi API de Muebleria'
#         })

#     elif request.method == 'POST':
#         # comportamiento cuando sea POST
#         return Response(data={
#             'message': 'Hiciste un post'
#         }, status=201)
class RegistroUsuarioApiView(CreateAPIView):   
    serializer_class=RegistroUsuarioSeriaizer
    def post(self,request:Request):
        data=self.serializer_class(data=request.data)
        data.is_valid(raise_exception=True)
        data.save()
        return Response(
            data={
                'message':'Usuario creado exitosmente',
                'content':data.data
            },
            status=status.HTTP_201_CREATED
        )