from abc import abstractmethod, ABC
import re


class Builder(ABC):

    @abstractmethod
    def get_product(self):
        pass

    @abstractmethod
    def build_header(self):
        pass

    @abstractmethod
    def build_script(self):
        pass


class TemplateBuilder(Builder):
    """ Klasa koja pravi output templejt

    Attributes
    -----------
    plugin : PrikazatiService
        plugin za prikaz
    product : string
        tekst templejta koji ce se renderovati
    """

    def __init__(self, plugin):
        self.plugin = plugin
        self.product = ""

    def get_product(self):
        """ Vraca napravljeni proizvod
            i resetuje proizvod za potencijalno dalje koriscenje buildera

        Returns
        ---------
        ret : string
            tekst templejta koji ce se renderovati
        """

        ret = self.product
        self.product = ""
        return ret

    def build_header(self):
        """ Integrise head informacije na proizvod(templejt) """

        include = '{% extends "prikaz_komponenta.html" %}\n'
        head_content = '{% block head_sadrzaj %}\n <head>\n'
        end_head = '</head>\n {% endblock %}\n'

        self.product += include + head_content + \
                        self.plugin.vrati_head_sadrzaj() + end_head

    def build_script(self):
        """ Integrise javascript kod na proizvod(templejt) """

        script_block = '\n{% block component %}\n <script>\n'
        end_script = '</script>\n {% endblock %}\n'
        kod = self.plugin.vrati_kod()
        self.check_error(kod)
        self.product += script_block + kod + end_script

    def check_error(self, kod):
        """ Proverava da li kod iz plugina implementira interfejs za prikaz

        Parameters
        -----------
        kod : string
            kod plugina u tekstualnoj reprezentaciji

        Raises
        -----------
        e : Exception
            ako nije uspeo da pronadje fju za interfejs
        """

        # obrisi sve razmake
        no_spaces = kod.replace(" ", "")

        # pogledaj da li postoji draw funkcija sa tacno 3 parametra
        match = re.search("functiondraw\\([a-zA-z]+,[a-zA-z]+,[a-zA-z]+\\)", no_spaces)

        # ako je match None znaci da ne postoji
        if match is None:
            raise Exception('Morate u pluginu implementirati fju draw koja prima 3 parametra '
                            '(pogledajte dokumentaciju interfejsa sa prikaz)')
