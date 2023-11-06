from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.conf import settings
from django.views.generic import TemplateView
from Irori.models import Couleur, Competence, Equipement, Personnage,Caracteristique,Pouvoir,Village as ModelVillage, Quete, Qualite, LancerDes, Session
from random import randint
from statistics import mean 

from rest_framework.views import APIView
from rest_framework.response import Response

class Index(TemplateView):
    def get(self, request, **kwargs):
        return HttpResponseRedirect( settings.LOGIN_URL )

def createContextHub(username,id,version):
    villageJoueur = ModelVillage.objects.filter(Version=version)[0]
    persosJoueur = Personnage.objects.filter(Joueur=id)
    admUser = User.objects.filter(username="admmmenault")[0]
    personnagesJoueurs = Personnage.objects.all().exclude(Joueur__in=[admUser]).filter(Village=villageJoueur)
    pnj = Personnage.objects.filter(Joueur=admUser).filter(Village=villageJoueur)
    return {
            "username":username,
            "personnagesJoueur":persosJoueur,
            "personnagesJoueurs":personnagesJoueurs,
            "PNJ":pnj,
            "village":villageJoueur,
            "version":version
            }

class Hub(TemplateView):

    template_name = 'base.html'

    def get(self, request, **kwargs):
        return render(request, self.template_name,createContextHub(request.user.username,request.user.id,kwargs["version"]))

def createContextVillage(village_id,username,version):
    village = ModelVillage.objects.filter(id=village_id)[0]
    habitants = Personnage.objects.filter(Village=village_id)
    admUser = User.objects.filter(username="admmmenault")[0]
    personnagesJoueur = Personnage.objects.all().exclude(Joueur__in=[admUser]).filter(Village=village)
    pnj = Personnage.objects.filter(Joueur=admUser).filter(Village=village)
    inventaireVillage = Equipement.objects.filter(Village=village_id)
    quetesVillage = Quete.objects.filter(Village=village_id)
    quetesPouvoir = Quete.objects.filter(Type=3).filter(Version=version)
    return {
            "username":username,
            "village":village,
            "habitants":habitants,
            "inventaire":inventaireVillage,
            "quetes":quetesVillage,
            "quetesPouvoir":quetesPouvoir,
            "personnagesJoueur":personnagesJoueur,
            "PNJ":pnj,
            "version":version
        }

class Village(TemplateView):
    template_name = 'village.html'

    def get(self, request, **kwargs):
        return render(request, self.template_name,createContextVillage(kwargs["village_id"],request.user.username,kwargs["version"]))

class Fiches(TemplateView):
    template_name = 'fiches.html'

    def get(self, request, **kwargs):
        village = ModelVillage.objects.filter(Version=kwargs["version"])[0]
        persosJoueur = Personnage.objects.filter(Village=village)
        admUser = User.objects.filter(username="admmmenault")[0]
        personnagesJoueur = Personnage.objects.all().exclude(Joueur__in=[admUser]).filter(Village=village)
        pnj = Personnage.objects.filter(Joueur=admUser).filter(Village=village)
        return render(request, self.template_name, 
            {
                "username":request.user.username,
                "village":village,
                "personnages":persosJoueur,
                "personnagesJoueur":personnagesJoueur,
                "PNJ":pnj,
                "version":kwargs["version"]
                })

def createContext(perso_id,username,version):

    persoFiche = Personnage.objects.filter(id=perso_id)[0]
    admUser = User.objects.filter(username="admmmenault")[0]
    personnagesJoueur = Personnage.objects.all().exclude(Joueur__in=[admUser]).filter(Village=ModelVillage.objects.filter(Version=version)[0])
    pnj = Personnage.objects.filter(Joueur=admUser).filter(Village=ModelVillage.objects.filter(Version=version)[0])
    caracs = Caracteristique.objects.filter(Proprietaire=perso_id)
    pouvoirs = Pouvoir.objects.filter(Proprietaire=perso_id)
    inventaire = Equipement.objects.filter(Proprietaire=perso_id).filter(Statistique__icontains="N/A")
    armes = Equipement.objects.filter(Proprietaire=perso_id).filter(Statistique__icontains="d")
    armures = Equipement.objects.filter(Proprietaire=perso_id).filter(Statistique__icontains="p")
    competences = Competence.objects.filter(Categorie__in=caracs)
    quetes = Quete.objects.filter(Proprietaire=perso_id)
    return  {
            "username":username,
            "personnage":persoFiche,
            "personnagesJoueur":personnagesJoueur,
            "PNJ":pnj,
            "caracs":caracs,
            "competences":competences,
            "pouvoirs":pouvoirs,
            "inventaire":inventaire,
            "armes":armes,
            "armures":armures,
            "quetes":quetes,
            "resultat":-1,
            "version":version
            }

class FichePerso(TemplateView):

    template_name = 'fichePerso.html'

    def get(self, request, **kwargs):
        return render(request, self.template_name,createContext(kwargs["perso_id"],request.user.username,kwargs["version"]))


def saveLancer(joueur, resultat, bonus, taille, session, version, perso, action, des):
    lancer = LancerDes()
    lancer.Joueur = joueur
    lancer.Valeur = resultat
    lancer.Bonus = bonus
    lancer.Taille = taille
    lancer.Session = session
    lancer.Version = version
    lancer.Perso = perso
    lancer.Action = action
    lancer.Des = des
    lancer.save()
    return None

class lancerDes(TemplateView):
    
    template_name = 'fichePerso.html'

    def get(self, request, **kwargs):
        context = createContext(kwargs["perso_id"],request.user.username,kwargs["version"])
        context["resultat"] = randint(1,kwargs["taille_des"])+kwargs["carac_points"]
        context["resultat_brut"] = context["resultat"] - kwargs["carac_points"]
        context["bonus"] = kwargs["carac_points"]
        context["couleur_lancer"] = "success" if context["resultat_brut"] >= 19 else "danger" if context["resultat_brut"] <= 2 else "info"
        action = ""
        des = f"1d{kwargs['taille_des']}+{kwargs['carac_points']}"

        if kwargs["carac_id"] != 0 :
            carac = Caracteristique.objects.filter(id=kwargs["carac_id"])[0]
            if carac.Nom == "Force":
                action = "s'est servi de sa force"
            elif carac.Nom == "Constitution":
                action = "s'est servi de sa constitution"
            elif carac.Nom == "Dexterite":
                action = "s'est servi de sa dextérité"
            elif carac.Nom == "Intelligence":
                action = "s'est servi de son intelligence"
            elif carac.Nom == "Charisme":
                action = "s'est servi de son charisme"
            elif carac.Nom == "Chance":
                action = "s'est servi de sa chance"
            else:
                action = f"s'est servi de {carac.Nom}"
        elif kwargs["comp_id"] != 0 :
            comp = Competence.objects.filter(id=kwargs["comp_id"])[0]
            action = f"s'est servi de sa compétence {comp.Nom}"
        elif kwargs["pouvoir_id"] != 0 :
            pouvoir = Pouvoir.objects.filter(id=kwargs["pouvoir_id"])[0]
            action = f"s'est servi de son pouvoir {pouvoir.Nom}"
        else :
            action = "a obtenu "
        
        saveLancer(
            User.objects.filter(username=request.user.username)[0],
            context["resultat_brut"],
            kwargs["carac_points"],
            kwargs["taille_des"],
            Session.objects.filter(Version=kwargs["version"])[0].Numero,
            kwargs["version"],
            Personnage.objects.filter(id=kwargs["perso_id"])[0],
            action,
            des)

        return render(request, self.template_name,context)

class Attaquer(TemplateView):
    
    template_name = 'fichePerso.html'

    def post(self, request, **kwargs):

        context = createContext(kwargs["perso_id"],request.user.username,kwargs["version"])
        context["resultat"] = 0
        context["resultat_brut"] = ""
        context["bonus"] = 0
        context["couleur_lancer"] = "info"

        arme = Equipement.objects.all().filter(pk=kwargs["equipement_id"])[0]
        stat = arme.Statistique

        if "+" in stat:
            statSplit = stat.split("+")
        else:
            statSplit = [stat,0]

        bonus = statSplit[-1]
        context["bonus"] = bonus
        context["resultat"] = int(bonus)
        statSplit.pop()

        for lancerDe in statSplit:
            lancer = lancerDe.split("d")
            for i in range(0,int(lancer[0])):
                rdm = randint(1,int(lancer[1]))
                context["resultat"] = context["resultat"] + rdm
                if context["resultat_brut"] == "":
                    context["resultat_brut"] = str(rdm)
                else:
                    context["resultat_brut"] = context["resultat_brut"] + "+" + str(rdm)

        saveLancer(
            User.objects.filter(username=request.user.username)[0],
            context["resultat"],
            context["bonus"],
            -1,
            Session.objects.filter(Version=kwargs["version"])[0].Numero,
            kwargs["version"],
            Personnage.objects.filter(id=kwargs["perso_id"])[0],
            "a attaqué avec "+str(arme),
            str(stat))

        return render(request, self.template_name,context)

class createCompetence(TemplateView):

    template_name = 'fichePerso.html'
    
    def post(self, request, **kwargs):
        comp = Competence()
        proprio = Personnage.objects.filter(id=kwargs["perso_id"])[0]
        comp.Nom = request.POST["Nom_NEW"]
        comp.Bonus = request.POST["Bonus_NEW"]
        comp.Categorie = Caracteristique.objects.filter(Nom=request.POST["Categorie_NEW"]).filter(Proprietaire=proprio)[0]
        comp.save()
        return render(request, self.template_name,createContext(kwargs["perso_id"],request.user.username,kwargs["version"]))


class createEquipement(TemplateView):

    template_name = 'fichePerso.html'
    
    def post(self, request, **kwargs):
        objet = Equipement()
        objet.Nom = request.POST["Nom_NEW"]
        objet.Qualite = Qualite.objects.filter(Nom=request.POST["Qualite_NEW"])[0]
        objet.Quantite = request.POST["Quantite_NEW"]
        objet.Statistique = request.POST["Statistique_NEW"]
        objet.Proprietaire = Personnage.objects.filter(id=kwargs["perso_id"])[0]
        objet.save()
        return render(request, self.template_name,createContext(kwargs["perso_id"],request.user.username,kwargs["version"]))

class updateEquipement(TemplateView):

    template_name = 'fichePerso.html'
    
    def post(self, request, **kwargs):
        objet = Equipement.objects.get(pk=kwargs["equipement_id"])
        objet.Nom = request.POST["Nom_"+str(kwargs["equipement_id"])]
        objet.Qualite = Qualite.objects.filter(Nom=request.POST["Qualite_"+str(kwargs["equipement_id"])])[0]
        objet.Quantite = request.POST["Quantite_"+str(kwargs["equipement_id"])]
        objet.Statistique = request.POST["Statistique_"+str(kwargs["equipement_id"])]
        objet.save()
        return render(request, self.template_name,createContext(kwargs["perso_id"],request.user.username,kwargs["version"]))

class deleteEquipement(TemplateView):

    template_name = 'fichePerso.html'
    
    def post(self, request, **kwargs):
        objet = Equipement.objects.get(pk=kwargs["equipement_id"])
        objet.delete()
        return render(request, self.template_name,createContext(kwargs["perso_id"],request.user.username,kwargs["version"]))

class createEquipementVillage(TemplateView):

    template_name = 'village.html'
    
    def post(self, request, **kwargs):
        objet = Equipement()
        objet.Nom = request.POST["Nom_NEW"]
        objet.Qualite = Qualite.objects.filter(Nom=request.POST["Qualite_NEW"])[0]
        objet.Quantite = request.POST["Quantite_NEW"]
        objet.Statistique = request.POST["Statistique_NEW"]
        objet.Village = ModelVillage.objects.filter(id=kwargs["village_id"])[0]
        objet.save()
        return render(request, self.template_name,createContextVillage(kwargs["village_id"],request.user.username,kwargs["version"]))

class updateEquipementVillage(TemplateView):

    template_name = 'village.html'
    
    def post(self, request, **kwargs):
        objet = Equipement.objects.get(pk=kwargs["equipement_id"])
        objet.Nom = request.POST["Nom_"+str(kwargs["equipement_id"])]
        objet.Qualite = Qualite.objects.filter(Nom=request.POST["Qualite_"+str(kwargs["equipement_id"])])[0]
        objet.Quantite = request.POST["Quantite_"+str(kwargs["equipement_id"])]
        objet.Statistique = request.POST["Statistique_"+str(kwargs["equipement_id"])]
        objet.save()
        return render(request, self.template_name,createContextVillage(kwargs["village_id"],request.user.username,kwargs["version"]))

class deleteEquipementVillage(TemplateView):

    template_name = 'village.html'
    
    def post(self, request, **kwargs):
        objet = Equipement.objects.get(pk=kwargs["equipement_id"])
        objet.delete()
        return render(request, self.template_name,createContextVillage(kwargs["village_id"],request.user.username,kwargs["version"]))

class plusCompetence(TemplateView):

    template_name = 'fichePerso.html'
    
    def get(self, request, **kwargs):
        comp = Competence.objects.get(pk=kwargs["carac_id"])
        comp.Bonus = comp.Bonus + 1
        comp.save()
        return render(request, self.template_name,createContext(kwargs["perso_id"],request.user.username,kwargs["version"]))

class moinsCompetence(TemplateView):

    template_name = 'fichePerso.html'
    
    def get(self, request, **kwargs):
        comp = Competence.objects.get(pk=kwargs["carac_id"])
        comp.Bonus = comp.Bonus - 1
        comp.save()
        return render(request, self.template_name,createContext(kwargs["perso_id"],request.user.username,kwargs["version"]))

class plusCarac(TemplateView):

    template_name = 'fichePerso.html'
    
    def get(self, request, **kwargs):
        carac = Caracteristique.objects.get(pk=kwargs["carac_id"])
        carac.Points = carac.Points + 1
        carac.save()
        return render(request, self.template_name,createContext(kwargs["perso_id"],request.user.username,kwargs["version"]))

class moinsCarac(TemplateView):

    template_name = 'fichePerso.html'
    
    def get(self, request, **kwargs):
        carac = Caracteristique.objects.get(pk=kwargs["carac_id"])
        carac.Points = carac.Points - 1
        carac.save()
        return render(request, self.template_name,createContext(kwargs["perso_id"],request.user.username,kwargs["version"]))

def creerContextCreerPerso(username,version):
    village = ModelVillage.objects.filter(Version=version)[0]
    persosJoueur = Personnage.objects.all()
    admUser = User.objects.filter(username="admmmenault")[0]
    personnagesJoueur = Personnage.objects.all().exclude(Joueur__in=[admUser]).filter(Village=village)
    pnj = Personnage.objects.filter(Joueur=admUser).filter(Village=village)
    joueurs = User.objects.all()
    villages = ModelVillage.objects.filter(Version=version)
    return {
            "username":username,
            "village":village,
            "personnages":persosJoueur,
            "personnagesJoueur":personnagesJoueur,
            "PNJ":pnj,
            "Joueurs":joueurs,
            "Villages":villages,
            "version":version
            }

class creerPerso(TemplateView):

    template_name = 'creerPerso.html'
    
    def get(self, request, **kwargs):
        return render(request, self.template_name,creerContextCreerPerso(request.user.username,kwargs["version"]))

class creerPersoSave(TemplateView):

    template_name = 'creerPerso.html'

    def post(self, request, **kwargs):

        # Creer perso
        nouveauPerso = Personnage()
        nouveauPerso.Joueur = User.objects.filter(username=request.POST["Joueur"])[0]
        nouveauPerso.Village = ModelVillage.objects.filter(Nom=request.POST["Village"])[0]
        nouveauPerso.Prenom = request.POST["Prenom"]
        nouveauPerso.Nom = request.POST["Nom"]
        nouveauPerso.Age = request.POST["Age"]
        nouveauPerso.Sexe = request.POST["Sexe"]
        nouveauPerso.Nationalite = request.POST["Nationalite"]
        nouveauPerso.Personnalite = request.POST["Personnalite"]
        nouveauPerso.Profession = request.POST["Profession"]
        nouveauPerso.Role = request.POST["Role"]
        nouveauPerso.Specialite = request.POST["Specialite"]
        nouveauPerso.Aime = request.POST["Aime"]
        nouveauPerso.Deteste = request.POST["Deteste"]
        nouveauPerso.PointsMax = request.POST["PointsMax"]
        nouveauPerso.save()

        # Force
        force = Caracteristique()
        force.Proprietaire = nouveauPerso
        force.Nom = "Force"
        force.Points = request.POST["Force"]
        force.PointsMax = request.POST["Force"]
        force.Couleur = Couleur.objects.filter(Nom="Danger")[0]
        force.save()

        # Constitution
        constitution = Caracteristique()
        constitution.Proprietaire = nouveauPerso
        constitution.Nom = "Constitution"
        constitution.Points = request.POST["Constitution"]
        constitution.PointsMax = request.POST["Constitution"]
        constitution.Couleur = Couleur.objects.filter(Nom="Link")[0]
        constitution.save()

        # Dexterite
        dexterite = Caracteristique()
        dexterite.Proprietaire = nouveauPerso
        dexterite.Nom = "Dexterite"
        dexterite.Points = request.POST["Dexterite"]
        dexterite.PointsMax = request.POST["Dexterite"]
        dexterite.Couleur = Couleur.objects.filter(Nom="Success")[0]
        dexterite.save()

        # Intelligence
        intelligence = Caracteristique()
        intelligence.Proprietaire = nouveauPerso
        intelligence.Nom = "Intelligence"
        intelligence.Points = request.POST["Intelligence"]
        intelligence.PointsMax = request.POST["Intelligence"]
        intelligence.Couleur = Couleur.objects.filter(Nom="Primary")[0]
        intelligence.save()

        # Charisme
        charisme = Caracteristique()
        charisme.Proprietaire = nouveauPerso
        charisme.Nom = "Charisme"
        charisme.Points = request.POST["Charisme"]
        charisme.PointsMax = request.POST["Charisme"]
        charisme.Couleur = Couleur.objects.filter(Nom="Warning")[0]
        charisme.save()

        # Pouvoir
        pouvoir = Caracteristique()
        pouvoir.Proprietaire = nouveauPerso
        pouvoir.Nom = "Pouvoir"
        pouvoir.Points = request.POST["Pouvoir"]
        pouvoir.PointsMax = request.POST["Pouvoir"]
        pouvoir.Couleur = Couleur.objects.filter(Nom="Info")[0]
        pouvoir.save()

        # Chance
        chance = Caracteristique()
        chance.Proprietaire = nouveauPerso
        chance.Nom = "Chance"
        chance.Points = request.POST["Chance"]
        chance.PointsMax = request.POST["Chance"]
        chance.Couleur = Couleur.objects.filter(Nom="Grey-light")[0]
        chance.save()

        # PV
        pv = Caracteristique()
        pv.Proprietaire = nouveauPerso
        pv.Nom = "PV"
        pv.Points = request.POST["PV"]
        pv.PointsMax = request.POST["PV"]
        pv.Couleur = Couleur.objects.filter(Nom="Success-dark")[0]
        pv.save()

        # PP
        pp = Caracteristique()
        pp.Proprietaire = nouveauPerso
        pp.Nom = "PP"
        pp.Points = request.POST["PP"]
        pp.PointsMax = request.POST["PP"]
        pp.Couleur = Couleur.objects.filter(Nom="Link-dark")[0]
        pp.save()

        # Moral
        moral = Caracteristique()
        moral.Proprietaire = nouveauPerso
        moral.Nom = "Moral"
        moral.Points = request.POST["Moral"]
        moral.PointsMax = request.POST["Moral"]
        moral.Couleur = Couleur.objects.filter(Nom="Primary-dark")[0]
        moral.save()

        # Création du pouvoir
        pouvoirPerso = Pouvoir()
        pouvoirPerso.Proprietaire = nouveauPerso
        pouvoirPerso.Nom = request.POST["NomPouvoir"]
        pouvoirPerso.Description = request.POST["DescriptionPouvoir"]
        pouvoirPerso.Niveau = request.POST["NiveauPouvoir"]
        pouvoirPerso.Cout = request.POST["CoutPouvoir"]
        pouvoirPerso.save()

        return render(request, self.template_name,creerContextCreerPerso(request.user.username,kwargs["version"]))

class statsDes(TemplateView):
    
    template_name = 'statsDes.html'

    def get(self, request, **kwargs):
        context = creerContextCreerPerso(request.user.username,kwargs["version"])
        joueurs = User.objects.all().order_by('first_name')
        context["Joueurs"] = joueurs
        context["LancersParSession"] = []
        context["MoyennesParSession"] = []
        context["Moins10ParSession"] = []
        context["EchecsParSession"] = []
        context["ReussitesParSession"] = []
        context["version"] = kwargs["version"]
        sessionCourante = Session.objects.filter(Version=kwargs["version"])[0]
        for i in range(1,sessionCourante.Numero+1):
            lancers = LancerDes.objects.filter(Session=i).filter(Taille=20).filter(Version=kwargs["version"])

            lancersAndrea = lancers.filter(Joueur=joueurs.filter(username="CORDEROCKET")[0]).filter(Taille=20)
            lancersAndreaMoins10 = lancersAndrea.filter(Valeur__lte=10)
            lancersAndreaEchec = lancersAndrea.filter(Valeur__lte=2)
            lancersAndreaReussite = lancersAndrea.filter(Valeur__gte=19)

            lancersAnthony = lancers.filter(Joueur=joueurs.filter(username="PeteurDeLattes")[0]).filter(Taille=20)
            lancersAnthonyMoins10 = lancersAnthony.filter(Valeur__lte=10)
            lancersAnthonyEchec = lancersAnthony.filter(Valeur__lte=2)
            lancersAnthonyReussite = lancersAnthony.filter(Valeur__gte=19)

            lancersAntonin = lancers.filter(Joueur=joueurs.filter(username="Warns")[0]).filter(Taille=20)
            lancersAntoninMoins10 = lancersAntonin.filter(Valeur__lte=10)
            lancersAntoninEchec = lancersAntonin.filter(Valeur__lte=2)
            lancersAntoninReussite = lancersAntonin.filter(Valeur__gte=19)

            lancersGautier = lancers.filter(Joueur=joueurs.filter(username="Rouguail")[0]).filter(Taille=20)
            lancersGautierMoins10 = lancersGautier.filter(Valeur__lte=10)
            lancersGautierEchec = lancersGautier.filter(Valeur__lte=2)
            lancersGautierReussite = lancersGautier.filter(Valeur__gte=19)

            lancersMaxime = lancers.filter(Joueur=joueurs.filter(username="admmmenault")[0]).filter(Taille=20)
            lancersMaximeMoins10 = lancersMaxime.filter(Valeur__lte=10)
            lancersMaximeEchec = lancersMaxime.filter(Valeur__lte=2)
            lancersMaximeReussite = lancersMaxime.filter(Valeur__gte=19)

            context["LancersParSession"].append({
                "session":f"Session {i}",
                "Andrea":len(lancersAndrea) if len(lancersAndrea) > 0 else '-',
                "Anthony":len(lancersAnthony) if len(lancersAnthony) > 0 else '-',
                "Antonin":len(lancersAntonin) if len(lancersAntonin) > 0 else '-',
                "Gautier":len(lancersGautier) if len(lancersGautier) > 0 else '-',
                "Maxime":len(lancersMaxime) if len(lancersMaxime) > 0 else '-'
            })
            context["MoyennesParSession"].append({
                "session":f"Session {i}",
                "Andrea":round(mean(lancer.Valeur for lancer in lancersAndrea),2) if len(lancersAndrea) > 0 else '-',
                "Anthony":round(mean(lancer.Valeur for lancer in lancersAnthony),2) if len(lancersAnthony) > 0 else '-',
                "Antonin":round(mean(lancer.Valeur for lancer in lancersAntonin),2) if len(lancersAntonin) > 0 else '-',
                "Gautier":round(mean(lancer.Valeur for lancer in lancersGautier),2) if len(lancersGautier) > 0 else '-',
                "Maxime":round(mean(lancer.Valeur for lancer in lancersMaxime),2) if len(lancersMaxime) > 0 else '-'
            })
            context["Moins10ParSession"].append({
                "session":f"Session {i}",
                "Andrea":f"{round((len(lancersAndreaMoins10)/len(lancersAndrea))*100,2)}%" if len(lancersAndreaMoins10) > 0 else '-',
                "Anthony":f"{round((len(lancersAnthonyMoins10)/len(lancersAnthony))*100,2)}%" if len(lancersAnthonyMoins10) > 0 else '-',
                "Antonin":f"{round((len(lancersAntoninMoins10)/len(lancersAntonin))*100,2)}%" if len(lancersAntoninMoins10) > 0 else '-',
                "Gautier":f"{round((len(lancersGautierMoins10)/len(lancersGautier))*100,2)}%" if len(lancersGautierMoins10) > 0 else '-',
                "Maxime":f"{round((len(lancersMaximeMoins10)/len(lancersMaxime))*100,2)}%" if len(lancersMaximeMoins10) > 0 else '-'
            })
            context["EchecsParSession"].append({
                "session":f"Session {i}",
                "Andrea":len(lancersAndreaEchec) if len(lancersAndreaEchec) > 0 else '-',
                "Anthony":len(lancersAnthonyEchec) if len(lancersAnthonyEchec) > 0 else '-',
                "Antonin":len(lancersAntoninEchec) if len(lancersAntoninEchec) > 0 else '-',
                "Gautier":len(lancersGautierEchec) if len(lancersGautierEchec) > 0 else '-',
                "Maxime":len(lancersMaximeEchec) if len(lancersMaximeEchec) > 0 else '-'
            })
            context["ReussitesParSession"].append({
                "session":f"Session {i}",
                "Andrea":len(lancersAndreaReussite) if len(lancersAndreaReussite) > 0 else '-',
                "Anthony":len(lancersAnthonyReussite) if len(lancersAnthonyReussite) > 0 else '-',
                "Antonin":len(lancersAntoninReussite) if len(lancersAntoninReussite) > 0 else '-',
                "Gautier":len(lancersGautierReussite) if len(lancersGautierReussite) > 0 else '-',
                "Maxime":len(lancersMaximeReussite) if len(lancersMaximeReussite) > 0 else '-'
            })

        lancersAndrea = LancerDes.objects.filter(Joueur=joueurs.filter(username="CORDEROCKET")[0]).filter(Version=kwargs["version"]).filter(Taille=20)
        lancersAndreaMoins10 = lancersAndrea.filter(Valeur__lte=10)
        lancersAndreaEchec = lancersAndrea.filter(Valeur__lte=2)
        lancersAndreaReussite = lancersAndrea.filter(Valeur__gte=19)

        lancersAnthony = LancerDes.objects.filter(Joueur=joueurs.filter(username="PeteurDeLattes")[0]).filter(Version=kwargs["version"]).filter(Taille=20)
        lancersAnthonyMoins10 = lancersAnthony.filter(Valeur__lte=10)
        lancersAnthonyEchec = lancersAnthony.filter(Valeur__lte=2)
        lancersAnthonyReussite = lancersAnthony.filter(Valeur__gte=19)

        lancersAntonin = LancerDes.objects.filter(Joueur=joueurs.filter(username="Warns")[0]).filter(Version=kwargs["version"]).filter(Taille=20)
        lancersAntoninMoins10 = lancersAntonin.filter(Valeur__lte=10)
        lancersAntoninEchec = lancersAntonin.filter(Valeur__lte=2)
        lancersAntoninReussite = lancersAntonin.filter(Valeur__gte=19)

        lancersGautier = LancerDes.objects.filter(Joueur=joueurs.filter(username="Rouguail")[0]).filter(Version=kwargs["version"]).filter(Taille=20)
        lancersGautierMoins10 = lancersGautier.filter(Valeur__lte=10)
        lancersGautierEchec = lancersGautier.filter(Valeur__lte=2)
        lancersGautierReussite = lancersGautier.filter(Valeur__gte=19)

        lancersMaxime = LancerDes.objects.filter(Joueur=joueurs.filter(username="admmmenault")[0]).filter(Version=kwargs["version"]).filter(Taille=20)
        lancersMaximeMoins10 = lancersMaxime.filter(Valeur__lte=10)
        lancersMaximeEchec = lancersMaxime.filter(Valeur__lte=2)
        lancersMaximeReussite = lancersMaxime.filter(Valeur__gte=19)
        
        context["TotalLancers"] = {
            "Andrea":len(lancersAndrea),
            "Anthony":len(lancersAnthony),
            "Antonin":len(lancersAntonin),
            "Gautier":len(lancersGautier),
            "Maxime":len(lancersMaxime)
        }

        context["TotalMoyenne"] = {
            "Andrea":round(mean(lancer.Valeur for lancer in lancersAndrea),2) if len(lancersAndrea) > 0 else '-',
            "Anthony":round(mean(lancer.Valeur for lancer in lancersAnthony),2) if len(lancersAnthony) > 0 else '-',
            "Antonin":round(mean(lancer.Valeur for lancer in lancersAntonin),2) if len(lancersAntonin) > 0 else '-',
            "Gautier":round(mean(lancer.Valeur for lancer in lancersGautier),2) if len(lancersGautier) > 0 else '-',
            "Maxime":round(mean(lancer.Valeur for lancer in lancersMaxime),2) if len(lancersMaxime) > 0 else '-'
        }

        context["TotalMoins10"] = {
            "Andrea":f"{round((len(lancersAndreaMoins10)/len(lancersAndrea))*100,2)}%" if len(lancersAndreaMoins10) > 0 else '-',
            "Anthony":f"{round((len(lancersAnthonyMoins10)/len(lancersAnthony))*100,2)}%" if len(lancersAnthonyMoins10) > 0 else '-',
            "Antonin":f"{round((len(lancersAntoninMoins10)/len(lancersAntonin))*100,2)}%" if len(lancersAntoninMoins10) > 0 else '-',
            "Gautier":f"{round((len(lancersGautierMoins10)/len(lancersGautier))*100,2)}%" if len(lancersGautierMoins10) > 0 else '-',
            "Maxime":f"{round((len(lancersMaximeMoins10)/len(lancersMaxime))*100,2)}%" if len(lancersMaximeMoins10) > 0 else '-'
        }

        context["TotalEchec"] = {
            "Andrea":len(lancersAndreaEchec) if len(lancersAndreaEchec) > 0 else '-',
            "Anthony":len(lancersAnthonyEchec) if len(lancersAnthonyEchec) > 0 else '-',
            "Antonin":len(lancersAntoninEchec) if len(lancersAntoninEchec) > 0 else '-',
            "Gautier":len(lancersGautierEchec) if len(lancersGautierEchec) > 0 else '-',
            "Maxime":len(lancersMaximeEchec) if len(lancersMaximeEchec) > 0 else '-'
        }

        context["TotalReussite"] = {
            "Andrea":len(lancersAndreaReussite) if len(lancersAndreaReussite) > 0 else '-',
            "Anthony":len(lancersAnthonyReussite) if len(lancersAnthonyReussite) > 0 else '-',
            "Antonin":len(lancersAntoninReussite) if len(lancersAntoninReussite) > 0 else '-',
            "Gautier":len(lancersGautierReussite) if len(lancersGautierReussite) > 0 else '-',
            "Maxime":len(lancersMaximeReussite) if len(lancersMaximeReussite) > 0 else '-'
        }

        context["TotalEchecPourcent"] = {
            "Andrea":f"{round((len(lancersAndreaEchec)/len(lancersAndrea))*100,2)}%" if len(lancersAndreaEchec) > 0 else '-',
            "Anthony":f"{round((len(lancersAnthonyEchec)/len(lancersAnthony))*100,2)}%" if len(lancersAnthonyEchec) > 0 else '-',
            "Antonin":f"{round((len(lancersAntoninEchec)/len(lancersAntonin))*100,2)}%" if len(lancersAntoninEchec) > 0 else '-',
            "Gautier":f"{round((len(lancersGautierEchec)/len(lancersGautier))*100,2)}%" if len(lancersGautierEchec) > 0 else '-',
            "Maxime":f"{round((len(lancersMaximeEchec)/len(lancersMaxime))*100,2)}%" if len(lancersMaximeEchec) > 0 else '-'
        }

        context["TotalReussitePourcent"] = {
            "Andrea":f"{round((len(lancersAndreaReussite)/len(lancersAndrea))*100,2)}%" if len(lancersAndreaReussite) > 0 else '-',
            "Anthony":f"{round((len(lancersAnthonyReussite)/len(lancersAnthony))*100,2)}%" if len(lancersAnthonyReussite) > 0 else '-',
            "Antonin":f"{round((len(lancersAntoninReussite)/len(lancersAntonin))*100,2)}%" if len(lancersAntoninReussite) > 0 else '-',
            "Gautier":f"{round((len(lancersGautierReussite)/len(lancersGautier))*100,2)}%" if len(lancersGautierReussite) > 0 else '-',
            "Maxime":f"{round((len(lancersMaximeReussite)/len(lancersMaxime))*100,2)}%" if len(lancersMaximeReussite) > 0 else '-'
        }

        return render(request, self.template_name,context)

class statsDesGet(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        joueurs = User.objects.all().order_by('first_name')
        data = []
        for joueur in joueurs:
            lancers = LancerDes.objects.filter(Joueur=joueur)
            if len(lancers) > 0:
                sessionMax = Session.objects.filter(Version=request.query_params.get("version"))[0].Numero
                labels=[]
                chartdata = []

                for i in range(1,(sessionMax+1)):
                    labels.append(f"Session {i}")
                    lancersSession = lancers.filter(Session=i).filter(Version=request.query_params.get("version"))

                    if len(lancersSession) > 0:
                        chartdata.append(mean(lancerSession.Valeur for lancerSession in lancersSession))
                    else:
                        chartdata.append(0)

                data.append({
                    "chartLabel":f"{joueur.first_name}",
                    "chartdata":chartdata,
                    "labels":labels
                })

        return Response(data)


class LoginView(TemplateView):

    template_name = "login.html"

    def post(self, request, **kwargs):

        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect( settings.LOGIN_REDIRECT_URL )
        return render(request, self.template_name)

class LogoutView(TemplateView):

  template_name = 'login.html'

  def get(self, request, **kwargs):

    logout(request)
    return HttpResponseRedirect( settings.LOGIN_URL )
