# commands/load_pokemons.py

from django.core.management.base import BaseCommand
from pokemon_app.models import Pokemon

class Command(BaseCommand):
    help = 'Load pokemons from a CSV file into the database'

    def handle(self, *args, **options):
        # Logique pour lire le fichier CSV et charger les données
        pass
