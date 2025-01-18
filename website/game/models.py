from django.db import models

class Tile(models.Model):
    row = models.IntegerField()
    column = models.IntegerField()
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"({self.row}, {self.column}), Value: {self.value}"

class Player(models.Model):
    name = models.CharField(max_length=100, default="One", unique=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}, Score: {self.score}"
