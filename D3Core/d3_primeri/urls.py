from django.urls import path

from d3_primeri import prodavnica_view

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('prikaz/plugin/<str:id>', views.ucitavanje_plugin, name="ucitavanje_plugin"),
    path('primer1', views.primer1, name="primer1"),
    path('primer2', views.primer2, name="primer2"),
    path('primer3', views.primer3, name="primer3"),
    path('forceMOJ', views.forceMOJ, name="forceMOJ"),
    path('primer4', views.primer4, name="primer4"),

    path('primer/prodavnica/force/layout', prodavnica_view.foce_layout, name="prodavnica_force_layout"),
    path('primer/prodavnica/tree/layout', prodavnica_view.tree_layout, name="prodavnica_tree_layout"),

    path('primer/pan/zoom', views.primerPanZoom, name="primerPanZoom"),
]