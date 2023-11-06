from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Personnage(models.Model):
    Joueur = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Nom = models.CharField(max_length=64)
    Age = models.IntegerField()
    Sexe = models.CharField(max_length=64)
    Origine = models.CharField(max_length=64)
    Religion = models.CharField(max_length=64)
    DateCreation = models.DateField()
    Poids = models.IntegerField()
    Taille = models.FloatField()
    Yeux = models.CharField(max_length=64)
    Cheveux = models.CharField(max_length=64)
    Peau = models.CharField(max_length=64)
    Dextrie = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.Nom}"

class Caracteristiques(models.Model):
    Personnage = models.ForeignKey(Personnage, on_delete=models.CASCADE, null=True)
    Force = models.IntegerField()
    Dexterite = models.IntegerField()
    Constitution = models.IntegerField()
    Intelligence = models.IntegerField()
    Sagesse = models.IntegerField()
    Charisme = models.IntegerField()
    def __str__(self):
        return f"Caracteristiques de {self.Personnage.Nom}"