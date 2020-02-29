from abc import abstractmethod, ABC


class PrikazatiService(ABC):
    """ Interfejs za plugine za prikaz """

    @abstractmethod
    def naziv(self):
        """ Vraca naziv plugina za prikaz

        Returns
        ---------
        name : string
            naziv plugina (ono sto ce pisati na stranici prilikom izboru)
        """
        pass

    @abstractmethod
    def identifier(self):
        """ Vraca identifikator plugina za prikaz

        Returns
        ---------
        id : string
            identifikator plugina (mora biti jedinstven)
        """
        pass

    @abstractmethod
    def vrati_kod(self):
        """ Vraca kod plugina za prikaz koji mora
            imati implementiranu sledecu javascript metodu:

            draw = function draw(data, svg, container)
                data : JSON
                    ucitani podaci u obliku grafa {nodes : {}, links : {}}
                svg : SVGElement
                    svg Kontejner za graficke elemente
                container : SVGElement
                    <g> element unutar <svg> koji grupise kreirane elemente

        Returns
        ---------
        raw_text : string
            kod za izvrsenje u tekstualnom obliku
        """
        pass

    def vrati_head_sadrzaj(self):
        """ Vraca head sadrzaj plugina za eventualno menjanje css atributa
            dovoljno je da vrati prazan string ako nema head elementa
            ( Nije obavezno )

        Returns
        ---------
        raw_text : string
            head sadrzaj ili prazan string
        """
        return ""


