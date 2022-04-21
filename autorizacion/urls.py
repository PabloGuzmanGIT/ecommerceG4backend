from django.urls import path
from .views import RegistroUsuarioApiView
#me retrnara dos toeken de acceso y de refresh
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('register/', RegistroUsuarioApiView.as_view()),
    path('login/',TokenObtainPairView.as_view())
]
