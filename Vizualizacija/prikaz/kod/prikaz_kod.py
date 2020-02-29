
import os
from core_module.services.prikazati import PrikazatiService

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

# importuj modul gde se nalaze templejti
from prikaz import templates


class Prikazi(PrikazatiService):

    def __init__(self):
        self.raw_text = pkg_resources.read_text(templates, 'prikaz_obican.html')

    def naziv(self):
        return "Obican prikaz"

    def identifier(self):
        return "prikaz_obican"

    def vrati_tekst(self):
        template = pkg_resources.read_text(templates, 'prikaz_obican.html')
        return template

    def vrati_head_sadrzaj(self):
        self.raw_text = pkg_resources.read_text(templates, 'prikaz_obican.html')
        return ""

    def vrati_kod(self):
        start = self.raw_text.find('<script>')
        end = self.raw_text.find('</script>')
        return self.raw_text[start+8 : end-1]


