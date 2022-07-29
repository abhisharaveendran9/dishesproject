from django.db import models

# Create your models here.

class Dishes(models.Model):
    name=models.CharField(max_length=120)
    price=models.PositiveIntegerField()
    category=models.CharField(max_length=120)
    rating=models.FloatField()

    def __str__(self):
        return self.name