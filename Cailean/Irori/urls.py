from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = "Irori"

urlpatterns = [
    path('', views.Index.as_view()),
    path('Hub/<int:version>', login_required(views.Hub.as_view())),
    path('Login', views.LoginView.as_view()),
    path('Logout', views.LoginView.as_view()),
    path('Fiches/<int:version>',login_required(views.Fiches.as_view())),
    path('Fiche/<int:version>/<int:perso_id>',login_required(views.FichePerso.as_view())),
    path('Fiche/<int:version>/<int:perso_id>/Lancer/<int:taille_des>/<int:carac_points>/<int:carac_id>/<int:comp_id>/<int:pouvoir_id>',login_required(views.lancerDes.as_view())),
    path('Fiche/<int:version>/<int:perso_id>/Attaque/<int:equipement_id>',login_required(views.Attaquer.as_view())),
    path('Fiche/<int:version>/<int:perso_id>/Update/<int:equipement_id>',login_required(views.updateEquipement.as_view())),
    path('Fiche/<int:version>/<int:perso_id>/Delete/<int:equipement_id>',login_required(views.deleteEquipement.as_view())),
    path('Fiche/<int:version>/<int:perso_id>/Create',login_required(views.createEquipement.as_view())),
    path('Fiche/<int:version>/<int:perso_id>/NouvelleCompetence',login_required(views.createCompetence.as_view())),
    path('Fiche/<int:version>/<int:perso_id>/Carac/Plus/<int:carac_id>',login_required(views.plusCarac.as_view())),
    path('Fiche/<int:version>/<int:perso_id>/Carac/Moins/<int:carac_id>', login_required(views.moinsCarac.as_view())),
    path('Fiche/<int:version>/<int:perso_id>/Competence/Plus/<int:carac_id>',login_required(views.plusCompetence.as_view())),
    path('Fiche/<int:version>/<int:perso_id>/Competence/Moins/<int:carac_id>',login_required(views.moinsCompetence.as_view())),
    path('CreerPerso/<int:version>',login_required(views.creerPerso.as_view())),
    path('CreerPerso/<int:version>/Save',login_required(views.creerPersoSave.as_view())),
    path('Village/<int:version>/<int:village_id>',login_required(views.Village.as_view())),
    path('Village/<int:version>/<int:village_id>/Update/<int:equipement_id>',login_required(views.updateEquipementVillage.as_view())),
    path('Village/<int:version>/<int:village_id>/Delete/<int:equipement_id>',login_required(views.deleteEquipementVillage.as_view())),
    path('Village/<int:version>/<int:village_id>/Create',login_required(views.createEquipementVillage.as_view())),
    path('StatsDes/<int:version>',login_required(views.statsDes.as_view())),
    path('StatsDes/Get',login_required(views.statsDesGet.as_view())),
    path('Session/<int:version>',login_required(views.SessionView.as_view()))
]
