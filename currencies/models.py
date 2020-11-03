from django.db import models


class Currency(models.Model):
    charcode = models.CharField("Код валюты", max_length=10)
    name = models.CharField("Название валюты", max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Валюта"
        verbose_name_plural = "Валюты"
