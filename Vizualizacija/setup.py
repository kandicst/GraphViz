from setuptools import setup, find_packages

setup(
    name="prikaz-obican",
    version="0.1",
    packages=find_packages(),
    install_requires=['d3-primeri>=0.1'],
    entry_points = {
        'prikaz.obican':
            ['prikaz_kod=prikaz.kod.prikaz_kod:Prikazi'],
    },
    zip_safe=True
)