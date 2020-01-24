import pkg_resources
from django.apps import AppConfig


class D3PrimeriConfig(AppConfig):
    name = 'd3_primeri'         #preko ovoga cemo pristupati pluginima u prodavnica_view
    plugini_ucitavanje=[]

    plugin_prikaz = None

    def ready(self):
        self.plugini_ucitavanje = load_plugins("prodavnica.ucitati")
        self.plugin_prikaz = load_plugins('prikaz.obican')[0]

def load_plugins(oznaka):
    plugins = []
    for ep in pkg_resources.iter_entry_points(group=oznaka):
        try :
            p = ep.load()
        except:
            continue
        print("{} {}".format(ep.name, p))
        plugin = p()
        plugins.append(plugin)
    return plugins

def load_plugins_ucitavanje(oznaka) :
    pass