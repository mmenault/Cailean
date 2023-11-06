from django import forms
from .models import Caracteristique,Equipement,Competence

class CaracteristiqueForm(forms.ModelForm):
    class Meta:
        model = Caracteristique
        fields = ['Points', 'Couleur']

class EquipementForm(forms.ModelForm):
    class Meta:
        model = Equipement
        fields = ['Nom', 'Qualite', 'Quantite', 'Statistique']

class CompetenceForm(forms.ModelForm):
    class Meta:
        model = Competence
        fields = ['Categorie', 'Nom', 'Bonus']