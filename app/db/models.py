# models.py

from django.db import models

class Tari(models.Model):
    id = models.AutoField(primary_key=True)
    nume_tara = models.CharField(max_length=100, unique=True)
    latitudine = models.FloatField()
    longitudine = models.FloatField()

    def __str__(self):
        return self.nume_tara

class Orase(models.Model):
    id = models.AutoField(primary_key=True)
    # delete all entities that are tied to this country
    id_tara = models.ForeignKey(Tari, on_delete=models.CASCADE)
    nume_oras = models.CharField(max_length=100)
    latitudine = models.FloatField()
    longitudine = models.FloatField()

    class Meta:
        unique_together = ('id_tara', 'nume_oras')

    def __str__(self):
        return f"{self.nume_oras}, {self.id_tara}"

class Temperaturi(models.Model):
    id = models.AutoField(primary_key=True)
    valoare = models.FloatField()
    # auto added to the db
    timestamp = models.DateTimeField(auto_now_add=True)
    id_oras = models.ForeignKey(Orase, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('id_oras', 'timestamp')

    def __str__(self):
        return f"Temperatura în {self.id_oras} la {self.timestamp}: {self.valoare}"
