from setuptools import setup, find_packages

setup(
    name="prikaz-obican",
    version="0.1",
    packages=find_packages(),
    install_requires=['core-module>=0.1'],
    entry_points = {
        'prikaz':
            ['prikaz_obican=prikaz.kod.prikaz_kod:Prikazi'],
    },
    package_data={'prikaz': ['templates/*.html']},
    zip_safe=True
)