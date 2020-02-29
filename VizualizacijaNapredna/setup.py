from setuptools import setup, find_packages

setup(
    name="prikaz-napredan",
    version="0.1",
    packages=find_packages(),
    install_requires=['core-module>=0.1'],
    entry_points={
        'prikaz':
            ['prikaz_napredan=napredan_prikaz.kod.prikaz_kod:PrikaziNapredan'],
    },
    package_data={'napredan_prikaz': ['templates/*.html']},
    zip_safe=True
)
