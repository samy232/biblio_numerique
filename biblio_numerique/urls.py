from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from gestion import views as api_views # Tes vues API du TP3
from UI_Bibliotheque import views as ui_views # Tes nouvelles vues UI du TP4

# 1. Configuration du Router pour l'API REST (Données JSON)
router = routers.DefaultRouter()
router.register(r'auteurs', api_views.AuteurViewSet)
router.register(r'livres', api_views.LivreViewSet)
router.register(r'emprunts', api_views.EmpruntViewSet)

# 2. Définition des Patterns d'URL
urlpatterns = [
    # --- Interface d'administration Django ---
    path('admin/', admin.site.urls),

    # --- Routes de l'API REST (TP3) ---
    # Accessible via http://127.0.0.1:8000/api/
    path('api/', include(router.urls)), 

    # --- Routes de l'Interface Graphique (TP4) ---
    # Accessible via http://127.0.0.1:8000/ui/auteurs/
    path('ui/auteurs/', ui_views.liste_auteurs_ui, name='ui_auteurs'),
    
    # On ajoutera les autres plus tard (livres, emprunts)
    # path('ui/livres/', ui_views.liste_livres_ui, name='ui_livres'),
    path('ui/auteurs/', ui_views.liste_auteurs_ui, name='ui_auteurs'),
    path('ui/auteurs/creer/', ui_views.creer_auteur_ui, name='ui_creer_auteur'),
    path('ui/auteurs/supprimer/<int:id>/', ui_views.supprimer_auteur_ui, name='ui_supprimer_auteur'),
    path('ui/auteurs/modifier/<int:id>/', ui_views.modifier_auteur_ui, name='ui_modifier_auteur'),
    # Dans urlpatterns de biblio_numerique/urls.py
    path('ui/livres/', ui_views.liste_livres_ui, name='ui_livres'),
    path('ui/livres/creer/', ui_views.creer_livre_ui, name='ui_creer_livre'),
    path('ui/livres/supprimer/<int:id>/', ui_views.supprimer_livre_ui, name='ui_supprimer_livre'),
    path('ui/livres/modifier/<int:id>/', ui_views.modifier_livre_ui, name='ui_modifier_livre'),
    path('ui/emprunts/', ui_views.liste_emprunts_ui, name='ui_emprunts'),
    path('ui/emprunts/creer/', ui_views.creer_emprunt_ui, name='ui_creer_emprunt'),
    path('ui/emprunts/rendre/<int:id>/', ui_views.rendre_livre_ui, name='ui_rendre_livre'),

    
    path('admin/', admin.site.urls),
    path('', ui_views.accueil, name='accueil'), # Page d'accueil racine
    path('ui/', include('UI_Bibliotheque.urls')),    # Assure-toi que cette ligne est présente :
    path('accounts/', include('comptes.urls')),
]

