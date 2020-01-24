from django.apps.registry import apps
from django.shortcuts import render, redirect

from d3_primeri.models import Template


def index(request):
    plugini = apps.get_app_config('d3_primeri').plugini_ucitavanje
    return render(request,"index.html",{"title":"Index","plugini_ucitavanje":plugini})

def ucitavanje_plugin(request,id):
    request.session['izabran_plugin_ucitavanje']=id
    plugini=apps.get_app_config('d3_primeri').plugini_ucitavanje
    for i in plugini:
        if i.identifier() == id:
            i.ucitati()
    return redirect('index')

def primer1(request):
    plugini = apps.get_app_config('d3_primeri').plugini_ucitavanje
    return render(request,"primer1.html",{"title":"Primer1","plugini_ucitavanje":plugini})


def primer2(request):
    plugini = apps.get_app_config('d3_primeri').plugini_ucitavanje
    return render(request, "primer2.html", {"title": "Primer2","plugini_ucitavanje":plugini})


def primer3(request):
    plugini = apps.get_app_config('d3_primeri').plugini_ucitavanje
    return render(request, "primer3.html", {"title": "Primer3","plugini_ucitavanje":plugini})

def primer4(request):
    plugini = apps.get_app_config('d3_primeri').plugini_ucitavanje
    return render(request, "primer4.html", {"title": "Primer4","plugini_ucitavanje":plugini})

def forceMOJ(request):
    plugini = apps.get_app_config('d3_primeri').plugini_ucitavanje
    prikaz = apps.get_app_config('d3_primeri').plugin_prikaz
    prikaz.ucitati()
    tt = Template.objects.all()
    return render(request, "forceMOJ.html", {"title": "MOJE","plugini_ucitavanje":plugini, "plugin_prikaz":prikaz})

def primerPanZoom(request):
    plugini = apps.get_app_config('d3_primeri').plugini_ucitavanje
    return render(request, "primerPanZoom.html", {"title": "Primer Pan Zoom","plugini_ucitavanje":plugini})