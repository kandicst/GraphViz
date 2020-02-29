from core_module.models import Node, Attribute, Link
from core_module.services.ucitati import UcitatiService
try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources
import json

from ucitavanje_filmovi import data


class UcitatiFilmoveJSON(UcitatiService):

    def naziv(self):
        return "Ucitati filmove iz JSON-a"

    def identifier(self):
        return "ucitati_filmove_json"

    def ucitati(self, parameters):
        self._ucitaj_cvorove(*self.parse_parameters(parameters))

    def form_fields(self):
        return [{"type": "number", "id": "godina", "text": "Unesite godinu za filmove", "value" : 2000},
                {"type": "number", "id": "max_num", "text": "Max broj filmova (-1 za sve)", "value" : -1}]

    def _napravi_veze(self, cvorovi, cvor):
        for cvor_lista in cvorovi:
            link = Link(source=cvor_lista, target=cvor, weight=str((cvor.influence + cvor_lista.influence) / 2))
            link.save()

    def _ucitaj_cvorove(self,godina='2000', max_num=-1):
        print(godina)
        try:
            text = pkg_resources.read_text(data,godina + ".json")
        except:
            print("NEMA FAJLA")
            return

        recnik = json.loads(text)

        filmovi = recnik['filmovi']

        max_num = int(max_num)
        if 0 < max_num < len(filmovi):
            filmovi = filmovi[:max_num]

        Node.objects.all().delete()
        Link.objects.all().delete()
        Attribute.objects.all().delete()

        links = {}

        for film in filmovi:
            n = Node(name=film["title"])
            n.influence = film["popularity"]
            gener_id = film["genre_ids"][0]
            n.group = float(gener_id)
            n.save()

            date = Attribute(name="Release Date", value=film["release_date"], node_id=n.get_id())
            rate = Attribute(name="Rate", value=film["vote_average"], node_id=n.get_id())
            votes = Attribute(name="Votes", value=film["vote_count"], node_id=n.get_id())
            date.save()
            rate.save()
            votes.save()

            n.attributes.add(date)
            n.attributes.add(rate, votes)

            # Napravi recnik koje povezuje cvorove

            if (gener_id not in links):
                links[gener_id] = []
            else:
                self._napravi_veze(links[gener_id], n)
            links[gener_id].append(n)
