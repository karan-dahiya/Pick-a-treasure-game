from django.test import TestCase
from .models import Tile, Player
from django.test import Client
c = Client()
# Create your tests here.
class TestCases(TestCase):

    def test_2player(self):
        response = c.get("http://127.0.0.1:8000/game/create/")
        players = Player.objects.all()
        self.assertEqual(players.count(), 2)
        self.assertEqual(players[0].name, "One")
        self.assertEqual(players[1].name, "Two")

    def test_100tiles(self):
        response = c.get("http://127.0.0.1:8000/game/create/")
        tiles = Tile.objects.all()
        self.assertEqual(len(tiles), 100)

    def test_treasureCreated(self):
        response = c.get("http://127.0.0.1:8000/game/create/")
        tiles = Tile.objects.all()

        found_value_of_one = False
        for tile in tiles:
            if tile.value != '-':
                valueNum = int(tile.value)
                if valueNum == 1:
                    found_value_of_one = True
                    break

        self.assertTrue(found_value_of_one)

    def test_scoreUpdate(self):
        response = c.get("http://127.0.0.1:8000/game/create/")
        players = Player.objects.all()
        self.assertEqual(players[0].name, "One")

        initial_value = players[0].score
        treasure = Tile.objects.exclude(value = "-").first()

        response = c.get(f"http://127.0.0.1:8000/game/game/pick/{players[0].name}/{treasure.row}/{treasure.column}/")

        self.assertEqual(players[0].score, initial_value +int(treasure.value))
