from setuptools import setup, find_packages

setup(
    name="ucitavanje-github",
    version="0.1",
    packages=find_packages(),
    install_requires=['core-module>=0.1'],
    entry_points = {
        'ucitavanje':
            ['ucitavanje_github_usera=ucitavanje_github_users.ucitavanje.ucitavanje:UcitavanjeGithub'],
    },
    zip_safe=True
)