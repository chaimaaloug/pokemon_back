# models.py

from django.db import models

class Pokemon(models.Model):
    name = models.CharField(max_length=255)
    type1 = models.CharField(max_length=255)
    type2 = models.CharField(max_length=255, null=True, blank=True)
    # Autres champs en fonction de votre fichier CSV pokemons.csv

# class PokemonType(models.Model):
#     type_name = models.CharField(max_length=255)
#     # Efficacité contre d'autres types
#     # Par exemple :
#     against_water = models.FloatField(default=1.0)
#     # Et ainsi de suite pour les autres types

class PokemonType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    strong_against = models.ManyToManyField('self', symmetrical=False, related_name='weak_against', blank=True)

    def __str__(self):
        return self.name
