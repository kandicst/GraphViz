from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('ucitavanje/<str:id>/<str:parameters>/', views.ucitavanje_plugin, name="ucitavanje_plugin"),
    path('ucitavanje/<str:id>/', views.ucitavanje_plugin, name="ucitavanje_plugin_bez_param"),
    path('prikaz/<str:id>', views.prikaz_plugin, name="prikaz_plugin"),

    path('dobavi_podatke', views.dobavi_podatke, name='getGraph'),
    path('prikaz/', views.prikaz_komponenta, name="prikaz_komponenta"),

]