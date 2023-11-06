from django.contrib import admin
from .models import Qualite,Personnage,Caracteristique,Pouvoir,Competence,Equipement,Couleur,Village,TypeQuete,Quete,LancerDes,Session

# Register your models here.
admin.site.register(Qualite)
admin.site.register(Couleur)
admin.site.register(Village)
admin.site.register(Personnage)
admin.site.register(Caracteristique)
admin.site.register(Pouvoir)
admin.site.register(Competence)
admin.site.register(Equipement)
admin.site.register(TypeQuete)
admin.site.register(Quete)
admin.site.register(LancerDes)
admin.site.register(Session)
