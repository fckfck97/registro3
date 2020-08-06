from django.urls import path
from . import views



urlpatterns = [

	#urls de inicio obstetricia
    path('', views.Inicio.as_view(), name='inicio'),
    path('agregar/', views.Paciente_Create.as_view(), name='index_obs'),
    path('agregar/paciente/', views.Paciente_Modal.as_view(), name='paciente_create'),

    path('examen_fisico/', views.Examen_Fisico_Create.as_view(), name='examen_fisico'),
    path('buscar/', views.Buscar.as_view(), name='buscar_obs'),
    path('buscar/resultado/',views.Buscar_Paciente.as_view(), name='buscar_paciente'),
    path('reporte_examen_fisico/<int:pk>/<int:pk2>/', views.reporte_examen_fisico, name='reporte_examen_fisico'),
    #Urls de parto normal
    path('parto/new/',views.Parto_Create.as_view() , name='parto_new'),
    path('parto/orden_medica_parto/',views.Orden_Medica_Parto_Create.as_view(), name='orden_medica_parto'),
    path('parto/nota/',views.Nota_Parto_Create.as_view(), name='nota_parto'),
    #url pdf parto normal
    path('parto/reporte/<int:pk>/<int:pk2>/',views.reporte_historia, name='reporte_historia'),
    path('parto/nota/<int:pk>/<int:pk2>/', views.reporte_nota, name='reporte_nota'),
    path('parto/consentimiento/<int:pk>/<int:pk2>/', views.reporte_consentimiento, name='reporte_consentimiento'),
    path('parto/orden_medica/<int:pk>/<int:pk2>/', views.reporte_orden, name='reporte_orden'),
    path('parto/edit/<int:pk>/', views.edit_paciente,name='edit_paciente'),
    path('parto/eliminar/<int:pk>/<int:pk2>/', views.Eliminar_Paciente.as_view(),name='eliminar_paciente')


    ]

