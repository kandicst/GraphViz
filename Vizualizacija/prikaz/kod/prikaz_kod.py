

# if __name__ == '__main__':
#     from jinja2 import Template, Environment, FileSystemLoader
#
#     file_loader = FileSystemLoader('')
#     env = Environment(loader=file_loader)
#     template = env.get_template('forceMOJ.HTML')
#     output = template.render()
#     print(output)
import os

from d3_primeri.models import Template
from d3_primeri.services.ucitati import UcitatiService


class Prikazi(UcitatiService):
    def naziv(self):
        return "Ucitati template iz koda"
    def identifier(self):
        return "prikaz_kod"

    def ucitati(self):
        Template.objects.all().delete()

        files = os.listdir(os.curdir)  # files and directories

        with open('..//Vizualizacija//prikaz//kod//forceMOJ.html', 'r') as file:
            data = file.read()
            t1 = Template(sadrzaj=data)
            t1.save()


