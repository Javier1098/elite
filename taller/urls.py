from django.urls import path
from django.contrib.auth.views import LogoutView

from.import views
from django.conf import settings
from django.contrib.staticfiles.urls import static



urlpatterns = [
    
    #estas son las rutas de los tecnicos
    path('principal_tecni/', views.tecnicos, name='principal_tecni'),

    #Estas son las rutas de los vehiculos
    path('lista/', views.lista_vehiculos, name='lista'),
    path('crear/', views.crear_vehiculo, name='crear'),
    path('editar/<str:placa>/', views.editar_vehiculo, name='editar'),
    path('eliminar/<str:placa>/', views.eliminar_vehiculo, name='eliminar'),
    
    #estas son las rutas de las tareas
    
    path('tareas/',views.lista_tareas,name='lista_tareas'),
    path('tareas/nueva/<str:placa>/',views.crear_tarea,name='crear_tarea'),
    path('tareas/editar/<int:id>/', views.editar_tarea, name='editar_tarea'),
    path('tareas/eliminar/<int:id>/',views.eliminar_tarea, name='eliminar_tarea'),
    path('tareas/<int:tarea_id>/imagenes/',views.imagenes_tarea,name='imagenes_tarea'),
    path('tareas-finalizadas/<int:id>/imagenes/',views.imagenes_tarea_finalizada,name='imagenes_tarea_finalizada'),
    
    
    
    #Estas son las rutas de los administrativos
    path('principal_admin/', views.administrativos, name='principal_admin'),
    path('informe/pdf/', views.informe_tareas_pdf, name='informe_pdf'),
    path('informes/', views.informe_view, name='informes'),
    path('informe/excel/', views.informe_tareas_excel, name='informe_excel'),
    path('historial-eliminados/',views.historial_eliminados,name='historial_eliminados'),
    path('administrativo/clientes/', views.lista_vehiculos_admin, name='lista_clientes_admin'),
    path('Tareas_eliminadas/', views.historial_tareas_eliminadas, name= 'lista_tareas_eliminadas'),
    path('administrativo/tareas/',views.lista_tareas_admin,name='lista_tareas_admin'),
    path('tareas-finalizadas/',views.lista_tareas_finalizadas,name='lista_tareas_finalizadas'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)