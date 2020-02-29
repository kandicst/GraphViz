from django.apps.registry import apps
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from core_module.builder.Builder import TemplateBuilder
from core_module.builder.Director import Director
from core_module.services.prikazati import PrikazatiService
from core_module.models import Node, Link, Attribute


def index(request):
    """ Pocetna strana web aplikacije

    Parameters
    -------
    request : HttpRequest
        http zahtev za pocetnu stranicu

    Returns
    -------
    odgovor : HttpResponse
        vraca http odgovor koji ce u browseru prikazati pocetnu stranicu
    """
    plugini = apps.get_app_config('core_module').plugini_ucitavanje
    plugini_prikaz = apps.get_app_config('core_module').plugini_prikaz
    return render(request, "prikaz_komponenta.html",
                  {"title": "Index",
                   "plugini_ucitavanje": plugini,
                   "plugini_prikaz": plugini_prikaz,
                   "nodes": Node.objects.all(),
                   })


def prikaz_komponenta(request):
    """ Prikazivanje ucitanih podataka

    Parameters
    -------
    request : HttpRequest
        http zahtev za prikaz

    Returns
    -------
    odgovor : HttpResponse
        vraca http odgovor koji ce u browseru prikazati ucitane podatke
        ukoliko oni postoje i plugin koji ce ih prikazati
    """

    plugini = apps.get_app_config('core_module').plugini_ucitavanje
    plugini_prikaz = apps.get_app_config('core_module').plugini_prikaz
    plug_viz = apps.get_app_config('core_module').selected_view_plugin

    # ako ne postoji plugin za prikaz
    # napravi prazan template
    if plug_viz is None:
        template = "{% extends 'prikaz_komponenta.html' %} \n" \
                   "{% block head_sadrzaj %}\n" \
                   "{% endblock %} {% block component %} {% endblock %}"

        with open("..//Core//core_module//templates//Output.html", "w") as text_file:
            text_file.write(template)

    return render(request, "Output.html",
                  {"title": "GraphVizz",
                   "plugini_ucitavanje": plugini,
                   "plugini_prikaz": plugini_prikaz,
                   "nodes": Node.objects.all()})


def prikaz_plugin(request, id):
    """ Postavlja novi plugin za prikaz

    Parameters
    -------
    request : HttpRequest
        http zahtev za pocetnu stranicu
    id : string
        identifikator novog plugina za prikaz

    Returns
    -------
    odgovor : HttpRedirect
        preusmerava na prikaz
    """

    request.session['izabran_plugin_prikaz'] = id
    apps.get_app_config('core_module').select_view_plugin(id, request)
    plug_viz = apps.get_app_config('core_module').selected_view_plugin
    director = apps.get_app_config('core_module').director

    builder = TemplateBuilder(plug_viz)
    template = director.buildTemplate(builder)

    with open("..//Core//core_module//templates//Output.html", "w") as text_file:
        text_file.write(template)

    return redirect('prikaz_komponenta')


def ucitavanje_plugin(request, id, parameters=""):
    """ Postavlja novi plugin za ucitavanje

    Parameters
    -------
    request : HttpRequest
        http zahtev za pocetnu stranicu
    id : string
        identifikator novog plugina za prikaz
    parameters : dictionary
        recnik sa parametrima forme (ukoliko plugin ima te parametre)

    Returns
    -------
    odgovor : HttpRedirect
        preusmerava na pocetnu stranicu
    """

    request.session['izabran_plugin_ucitavanje'] = id
    plugini = apps.get_app_config('core_module').plugini_ucitavanje
    for i in plugini:
        if i.identifier() == id:
            request.session['plugin_ucitavanje_ime'] = i.naziv()
            i.ucitati(parameters)

    return redirect('/')


def dobavi_podatke(request):
    """ Vraca ucitane podatke

    Parameters
    -------
    request : HttpRequest
        http zahtev

    Returns
    -------
    odgovor : JsonResponse
        JSON datoteka sa strukturom grafa (nodes, links)
        format :
            { nodes : [{id, name, influence, group, bold (da li je selektovan cvor),
                        attributes: [{ node_id, name, value }] },
              links : [{id, source_id, target_weight, weight }]
            }
    """
    if len(apps.get_app_config('core_module').plugini_ucitavanje) == 0:
        return JsonResponse({})

    if 'plugin_prikaz_ime' not in request.session.keys():
        return JsonResponse({})

    if 'plugin_ucitavanje_ime' not in request.session.keys():
        return JsonResponse({})

    nodes = list(Node.objects.values())
    for node in nodes:
        x = Attribute.objects.filter(node_id=node['id'])
        node['attributes'] = list(x.values())

    links = list(Link.objects.values())
    #print(request.session['plugin_prikaz_ime'])
    return JsonResponse({"nodes": nodes, "links": links})
