from decimal import Decimal

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Attribute(models.Model):
    """ Dinamicki atribut cvora

    Attributes
    ---------
    name : string
        naziv atributa
    value : string
        vrednost atributa
    """
    node_id = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    value = models.CharField(max_length=30)

    def __str__(self):
        return str(self.name) + ":" + str(self.value)


class Node(models.Model):
    """ Model cvora u grafu

    Attributes
    ---------
    name : string
        naziv cvora
    attributes : Attribute
        recnik sa nazivom i vrednoscu atributa cvora
    influlence : float
        vaznost cvora u odnosu na ostale u grafu (vrednosti izmedju 30 i 70)
    group : int
        oznaka grupe kojoj cvor pripada
    """
    name = models.CharField(max_length=100)
    attributes = models.ManyToManyField(Attribute)
    influence = models.DecimalField(max_digits=8,decimal_places=2,
                                    validators=[MinValueValidator(Decimal('30')), MaxValueValidator(Decimal('70'))])
    group = models.IntegerField(primary_key=False)

    def get_id(self):
        return self.id

    def get_attributes(self):
        return self.attributes

    def get_links_to_this_node(self):
        return Link.objects.all().filter(target=self)

    def get_links_from_this_node(self):
        return Link.objects.all().filter(source=self)

    def __str__(self):
        return "ID:" + str(self.id) + "\nNaziv:" + str(self.name)


class Link(models.Model):
    """ Model veze(grane) u grafu koja spaja 2 cvora

    Attributes
    ---------
    source : string
        id prvog cvora
    target : string
        id drugog cvora
    weight : float
        'tezina' grane (vrednosti izmedju 30 i 70)
    """
    source = models.ForeignKey(Node, related_name="cvor1", on_delete=models.CASCADE)
    target = models.ForeignKey(Node, related_name="cvor2", on_delete=models.CASCADE)
    weight = models.DecimalField(max_digits=8, decimal_places=2,
                                 validators=[MinValueValidator(Decimal('30')), MaxValueValidator(Decimal('70'))])

    def __str__(self):
        return "Source" + str(self.source) + ", Target" + str(self.target)
