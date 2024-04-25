from django.db import models
from django.db.models import Sum


class Disease(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name

