from django.urls import path
from . import views


urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('home/', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('cerrar_sesion', views.cerrar_sesion, name='cerrar_sesion'),
    path('iniciar_sesion/', views.logear, name='iniciar_sesion'),
    path('clave_puerta/', views.crear_clave_puerta, name='clave_puerta'),
    path('lista_puerta/', views.lista_usuarios, name='lista_puerta'),
    path('actualizacion_clave/<int:id>', views.actualizar_clave, name='actualizar_clave'),
    path('verificacion_clave/', views.verificacion_clave, name='verificacion_clave'),
    path('verificacion/', views.lista_registro, name='verificacion'),
    path('prueba/', views.prueba_decorador, name='prueba'),
    path('actualizar_datos/', views.actualizar_datos, name='actualizar_datos'),
    path('modificar_permisos/', views.permisos_usuarios, name='modificar_permisos'),
    path('permisos_profesor/', views.permisos_profesor, name='modificar_permisos_profesor'),
    path('tarjeta_adquisicion/', views.clave_adquisicion, name='tarjeta_adquisicion'),
    path('tarjeta_adquisicion_valores/<str:mi_dato>/', views.clave_adquisicion_valores, name='tarjeta_adquisicion_valores'),
]