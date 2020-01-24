from d3_primeri.models import Prodavnica, Artikal, Template
from django.apps.registry import apps
from django.shortcuts import render


def foce_layout(request):
    plugini = apps.get_app_config('d3_primeri').plugini_ucitavanje
    plug_viz = apps.get_app_config('d3_primeri').plugin_prikaz
    plug_viz.ucitati()

    prodavnice=Prodavnica.objects.all()
    artikli=Artikal.objects.all()
    templ = Template.objects.all()[0]
    with open("..//D3Core//d3_primeri//templates//Output.html", "w") as text_file:
        text_file.write('{% extends "base.html" %}\n')
        text_file.write(templ.sadrzaj)

    return render(request,"Output.html",
                  {"title":"Primer prodavnica force layout",
                   "plugini_ucitavanje": plugini,
                   "prodavnice":prodavnice,
                   "artikli":artikli})

    # return render(request,"primerProdavnicaForceLayout.html",
    #               {"title":"Primer prodavnica force layout",
    #                "plugini_ucitavanje": plugini,
    #                "prodavnice":prodavnice,
    #                "artikli":artikli})

def tree_layout(request):
    plugini = apps.get_app_config('d3_primeri').plugini_ucitavanje
    prodavnice=Prodavnica.objects.all()
    artikli=Artikal.objects.all()
    return render(request,"primerProdavnicaTreeLayout.html",
                  {"title":"Primer prodavnica force layout",
                   "plugini_ucitavanje": plugini,
                   "prodavnice":prodavnice,
                   "artikli":artikli})