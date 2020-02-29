import pkg_resources
from django.apps import AppConfig

from core_module.builder.Director import Director


class CoreConfig(AppConfig):
    """ Klasa koja cuva metapodatke aplikacije

    Attributes
    ---------
    name : string
        naziv configa
    plugini_ucitavanje : array-like
        kolekcija ucitanih plugina za ucitavanje
    plugini_prikaz : array-like
        kolekcija ucitanih plugina za prikaz
    """

    name = 'core_module'
    plugini_ucitavanje = []
    director = Director()
    plugin_prikaz = None

    def ready(self):
        """ Zapocinje ucitavanje plugina """
        self.__selected_view_plugin = None
        self.plugini_ucitavanje = load_plugins("ucitavanje")
        self.plugini_prikaz = load_plugins('prikaz')

    def select_view_plugin(self, ime, request=None):
        """ Postavlja novi plugin za prikaz i vezuje ga za sesiju

        Parameters
        -----------
        ime : string
            naziv plugina
        request : django.http.request
            zahtev korisnika koji je postavio plugin
        """
        for plugin in self.plugini_prikaz:
            if plugin.identifier() == ime:
                if request is not None:
                    request.session['plugin_prikaz_ime'] = plugin.naziv()
                self.selected_view_plugin = plugin
                break

    @property
    def selected_view_plugin(self):
        return self.__selected_view_plugin

    @selected_view_plugin.setter
    def selected_view_plugin(self, value):
        self.__selected_view_plugin = value


def load_plugins(oznaka):
    """ Ucitava instalirane plugine

    Parameters
    -----------
    oznaka : string
        naziv entry-pointa plugina koje treba ucitati

    Returns
    --------
    plugins : array-like
        lista ucitanih plugina
    """
    plugins = []
    for ep in pkg_resources.iter_entry_points(group=oznaka):
        try:
            p = ep.load()
        except Exception as exc:
            print(exc)
            continue
        print("{} {}".format(ep.name, p))
        plugin = p()
        plugins.append(plugin)
    return plugins
