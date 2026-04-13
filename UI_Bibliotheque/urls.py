from django.urls import path
from . import views

urlpatterns = [
    path('livres/', views.liste_livres_ui, name='ui_livres'),
    path('auteurs/', views.liste_auteurs_ui, name='ui_auteurs'),
    path('emprunts/', views.liste_emprunts_ui, name='ui_emprunts'),
    # ... ajoute tes autres routes ici (creer, supprimer, etc.)
]