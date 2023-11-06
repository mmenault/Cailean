from django.views.generic import TemplateView
from django.shortcuts import render
from Seraptis.models import Personnage
# Create your views here.

class Hub(TemplateView):

    template_name = 'base.html'

    def get(self, request, **kwargs):
        persosJoueur = Personnage.objects.filter(Joueur=request.user.id)
        return render(request, self.template_name, 
            {
                "username":request.user.username,
                "personnagesJoueur":persosJoueur
                })