from setuptools import setup, find_packages

setup(
    name="ucitavanje-filmovi",
    version="0.1",
    packages=find_packages(),
    install_requires=['core-module>=0.1'],
    entry_points = {
        'ucitavanje':
            ['ucitati_filmove_json=ucitavanje_filmovi.kod.ucitavanje_kod:UcitatiFilmoveJSON'],
    },
    package_data = {'ucitavanje_filmovi' : ['data/*.json']},
    zip_safe=True
)