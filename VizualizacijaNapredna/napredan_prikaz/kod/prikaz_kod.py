from core_module.services.prikazati import PrikazatiService
try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

# importuj modul gde se nalaze templejti
from napredan_prikaz import templates


class PrikaziNapredan(PrikazatiService):

    def __init__(self):
        self.raw_text = pkg_resources.read_text(templates, 'napredni.html')

    def naziv(self):
        return "Napredan prikaz"

    def identifier(self):
        return "prikaz_napredan"

    def vrati_head_sadrzaj(self):
        self.raw_text = pkg_resources.read_text(templates, 'napredni.html')
        return ""

    def vrati_kod(self):
        start = self.raw_text.find('<script>')
        end = self.raw_text.find('</script>')
        return self.raw_text[start+8 : end-1]

    def vrati_tekst(self):
        template = pkg_resources.read_text(templates, 'napredni.html')
        return template

