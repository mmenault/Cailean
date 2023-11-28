from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Qualite(models.Model):
    Nom = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.Nom}"

class Couleur(models.Model):
    Nom = models.CharField(max_length=32)
    def __str__(self):
        return f"{self.Nom}"

class Village(models.Model):
    Nom = models.CharField(max_length=64)
    Version = models.IntegerField(default=4)
    def __str__(self):
        return f"{self.Nom}"

class Personnage(models.Model):
    Joueur= models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Village = models.ForeignKey(Village, on_delete=models.CASCADE, null=True)
    Prenom = models.CharField(max_length=64)
    Nom = models.CharField(max_length=64)
    Age = models.IntegerField()
    Sexe = models.CharField(max_length=64)
    Nationalite = models.CharField(max_length=64)
    Personnalite = models.CharField(max_length=64)
    Profession = models.CharField(max_length=64)
    Role = models.CharField(max_length=64, null=True)
    Specialite = models.CharField(max_length=64)
    Aime = models.CharField(max_length=64)
    Deteste = models.CharField(max_length=64)
    Cache = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.Prenom} {self.Nom}"

class Caracteristique(models.Model):
    Proprietaire = models.ForeignKey(Personnage, on_delete=models.CASCADE)
    Nom = models.CharField(max_length=64)
    Points = models.IntegerField()
    PointsMax = models.IntegerField(null=True)
    Couleur = models.ForeignKey(Couleur, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"{self.Nom} {self.Proprietaire}"

class Pouvoir(models.Model):
    Proprietaire = models.ForeignKey(Personnage, on_delete=models.CASCADE)
    Nom = models.CharField(max_length=64)
    Description = models.CharField(max_length=64)
    Niveau = models.IntegerField()
    Cout = models.IntegerField()
    def __str__(self):
        return f"{self.Nom} {self.Proprietaire}"

class Competence(models.Model):
    Categorie = models.ForeignKey(Caracteristique, on_delete=models.CASCADE)
    Nom = models.CharField(max_length=64)
    Bonus = models.IntegerField()
    def __str__(self):
        return f"{self.Nom} {self.Categorie}"

class Equipement(models.Model):
    Proprietaire = models.ForeignKey(Personnage, on_delete=models.CASCADE, blank=True, null=True)
    Village = models.ForeignKey(Village, on_delete=models.CASCADE, blank=True, null=True)
    Qualite = models.ForeignKey(Qualite, on_delete=models.CASCADE)
    Quantite = models.IntegerField(default=1)
    Nom = models.CharField(max_length=64)
    Statistique = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.Nom}"

class TypeQuete(models.Model):
    Nom = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.Nom}"

class Quete(models.Model):
    Type = models.ForeignKey(TypeQuete, on_delete=models.CASCADE)
    Proprietaire = models.ForeignKey(Personnage, on_delete=models.CASCADE, blank=True, null=True)
    Village = models.ForeignKey(Village, on_delete=models.CASCADE, blank=True, null=True)
    Version = models.IntegerField(default=4)
    Description = models.CharField(max_length=64)
    Statut = models.CharField(max_length=64)
    Recompense = models.CharField(max_length=64)
    def __str__(self):
        if self.Proprietaire != None:
            return f"{self.Proprietaire} : {self.Description}"
        elif self.Village != None:
            return f"{self.Village} : {self.Description}"
        else:
            return f"{self.Description}"

class LancerDes(models.Model):
    Joueur = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    Perso = models.ForeignKey(Personnage, on_delete=models.CASCADE, blank=True, null=True)
    Version = models.IntegerField(default=4)
    Valeur = models.IntegerField()
    Bonus = models.IntegerField(default=0)
    Taille = models.IntegerField(default=20)
    Session = models.IntegerField(default=1)
    Action = models.CharField(max_length=256,default="")
    Des = models.CharField(max_length=64,default="")
    Couleur = models.ForeignKey(Couleur, on_delete=models.CASCADE, null=True)
    def __str__(self):
        if self.Perso != None :
            return f"{self.Perso} {self.Action} : {self.Valeur + self.Bonus} ({self.Des})"
        else: 
            return f"{self.Joueur} : {self.Valeur}+{self.Bonus}/{self.Taille}"

class Session(models.Model):
    Numero = models.IntegerField(default=1)
    Version = models.IntegerField(default=4)
    def __str__(self):
        return f"Session Dr Stone {self.Version} : {self.Numero}"
