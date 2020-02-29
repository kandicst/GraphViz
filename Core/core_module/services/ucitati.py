from abc import abstractmethod, ABC


class UcitatiService(ABC):
    """ Interfejs za plugine za ucitavanje """

    @abstractmethod
    def naziv(self):
        """ Vraca naziv plugina

        Returns
        ---------
        name : string
            naziv plugina (ono sto ce pisati na stranici prilikom izboru)
        """
        pass

    @abstractmethod
    def identifier(self):
        """ Vraca identifikator plugina za ucitavanje

        Returns
        ---------
        id : string
            identifikator plugina (mora biti jedinstven)
        """
        pass

    @abstractmethod
    def ucitati(self, parameters):
        """ Ucitava podatke iz plugina u bazu

        Parameters
        ---------
        parameters : string
            identifikator plugina (mora biti jedinstven)
        """
        pass

    def form_fields(self):
        """ Definise strukturu prozora za unos informacija pri ucitavanju

        Returns
        ---------
        form : array-like
            lista recnika sa poljima potrebnim za definisanje html forme (type, id , text)

        Primer povratne vrednosti koja predstavlja polje za tekstualni unos :
            [{"type": "text", "id": "name_field", "text": "Name", "value" : default_value}]
        """
        return []

    def parse_parameters(self, parameters):
        """ Parisra parametre forme zadate od strane korisnika

        Parameters
        ---------
        parameters : string
            parametri forme u obliku naziv1=vrednost1&naziv2=vrednost2


        Returns
        ---------
        parameter_list : array-like
            lista parametra
        """

        parameter_list = []

        # moze da dobije prazan string za parametre ako
        # plugin nema formu
        if not parameters.strip():
            return parameter_list

        for parameter in parameters.split("&"):
            parameter_list.append(parameter.split("=")[1])

        return parameter_list
