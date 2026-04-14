import os
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

# Get API URL from environment variable (for Render deployment)
API_BASE_URL = os.environ.get('API_BASE_URL', 'http://localhost:8000')

API_URL = f'{API_BASE_URL}/api/auteurs/'
LIVRES_API_URL = f'{API_BASE_URL}/api/livres/'
EMPRUNTS_API_URL = f'{API_BASE_URL}/api/emprunts/'

def est_admin(user):
    return user.is_authenticated and user.is_staff

def liste_auteurs_ui(request):
    """Affiche la liste des auteurs en récupérant les données de l'API."""
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            auteurs = response.json()
        else:
            auteurs = []
            messages.error(request, "Erreur lors de la récupération des auteurs.")
    except requests.exceptions.ConnectionError:
        auteurs = []
        messages.error(request, "Impossible de se connecter à l'API. Vérifiez que le serveur tourne.")

    return render(request, 'auteurs.html', {'auteurs': auteurs})

@login_required(login_url='login')
def creer_auteur_ui(request):
    """Affiche le formulaire et envoie les données à l'API via POST."""
    if not request.user.is_staff:
        messages.error(request, "⚠️ Action interdite : Vous n'avez pas les droits d'administrateur.")
        return redirect('ui_auteurs')
    
    if request.method == 'POST':
        data = {
            "nom": request.POST.get('nom'),
            "prenom": request.POST.get('prenom'),
            "nationalite": request.POST.get('nationalite'),
            "date_naissance": request.POST.get('date_naissance'),
        }
        
        try:
            response = requests.post(API_URL, json=data)
            
            if response.status_code == 201:
                messages.success(request, "Auteur ajouté avec succès !")
                return redirect('ui_auteurs')
            else:
                messages.error(request, f"Erreur API : {response.text}")
        except requests.exceptions.ConnectionError:
            messages.error(request, "Erreur de connexion à l'API.")

    return render(request, 'creer_auteur.html')

@login_required(login_url='login')
def supprimer_auteur_ui(request, id):
    """Envoie une requête DELETE à l'API pour supprimer l'auteur."""
    if not request.user.is_staff:
        messages.error(request, "⚠️ Action interdite : Vous n'avez pas les droits d'administrateur.")
        return redirect('ui_auteurs')
    
    url_suppression = f"{API_URL}{id}/"
    
    try:
        response = requests.delete(url_suppression)
        
        if response.status_code == 204:
            messages.success(request, "Auteur supprimé avec succès.")
        else:
            messages.error(request, f"Erreur lors de la suppression : {response.status_code}")
    except requests.exceptions.ConnectionError:
        messages.error(request, "Erreur de connexion à l'API.")

    return redirect('ui_auteurs')

@login_required(login_url='login')
def modifier_auteur_ui(request, id):
    if not request.user.is_staff:
        messages.error(request, "⚠️ Action interdite : Vous n'avez pas les droits d'administrateur.")
        return redirect('ui_auteurs')
    
    url_auteur = f"{API_URL}{id}/"

    if request.method == 'GET':
        response = requests.get(url_auteur)
        if response.status_code == 200:
            auteur = response.json()
            return render(request, 'modifier_auteur.html', {'auteur': auteur})
        return redirect('ui_auteurs')

    if request.method == 'POST':
        data = {
            "nom": request.POST.get('nom'),
            "prenom": request.POST.get('prenom'),
            "nationalite": request.POST.get('nationalite'),
            "date_naissance": request.POST.get('date_naissance'),
        }
        response = requests.put(url_auteur, json=data)
        
        if response.status_code == 200:
            messages.success(request, "Auteur mis à jour !")
            return redirect('ui_auteurs')
        else:
            messages.error(request, "Erreur lors de la modification.")
            return redirect('ui_auteurs')

def liste_livres_ui(request):
    nb_visites = request.session.get('visites', 0) + 1
    request.session['visites'] = nb_visites

    try:
        response = requests.get(LIVRES_API_URL)
        livres = response.json() if response.status_code == 200 else []
    except:
        livres = []
        
    return render(request, 'livres.html', {
        'livres': livres,
        'visites': nb_visites
    })

@login_required(login_url='login')
def supprimer_livre_ui(request, id):
    if not request.user.is_staff:
        messages.error(request, "⚠️ Action interdite : Vous n'avez pas les droits d'administrateur.")
        return redirect('ui_livres')
    
    requests.delete(f"{LIVRES_API_URL}{id}/")
    return redirect('ui_livres')

@login_required(login_url='login')
def creer_livre_ui(request):
    if not request.user.is_staff:
        messages.error(request, "⚠️ Action interdite : Vous n'avez pas les droits d'administrateur.")
        return redirect('ui_livres')
    
    if request.method == 'POST':
        try:
            id_auteur = int(request.POST.get('auteur'))
            pages = int(request.POST.get('nombre_pages', 0))
        except (ValueError, TypeError):
            messages.error(request, "Données invalides pour l'auteur ou le nombre de pages.")
            return redirect('creer_livre_ui')

        data = {
            "titre": request.POST.get('titre'),
            "isbn": request.POST.get('isbn'),
            "date_publication": request.POST.get('date_publication'),
            "auteur": id_auteur,
            "nombre_pages": pages,
            "disponible": True
        }
        
        response = requests.post(LIVRES_API_URL, json=data)
        
        if response.status_code == 201:
            messages.success(request, "Livre ajouté avec succès !")
            return redirect('ui_livres')
        else:
            messages.error(request, f"Erreur API : {response.text}")
            print(f"ERREUR API (POST): {response.text}")

    try:
        aut_resp = requests.get(f'{API_BASE_URL}/api/auteurs/')
        auteurs = aut_resp.json() if aut_resp.status_code == 200 else []
    except Exception as e:
        auteurs = []
        messages.error(request, "Impossible de charger la liste des auteurs.")
    
    return render(request, 'creer_livre.html', {'auteurs': auteurs})

@login_required(login_url='login')
def modifier_livre_ui(request, id):
    if not request.user.is_staff:
        messages.error(request, "⚠️ Action interdite : Vous n'avez pas les droits d'administrateur.")
        return redirect('ui_livres')
    
    url_livre = f"{LIVRES_API_URL}{id}/"
    
    if request.method == 'POST':
        data = {
            "titre": request.POST.get('titre'),
            "isbn": request.POST.get('isbn'),
            "date_publication": request.POST.get('date_publication'),
            "auteur": request.POST.get('auteur'),
            "nombre_pages": request.POST.get('nombre_pages', 0),
            "disponible": True
        }
        response = requests.put(url_livre, json=data)
        if response.status_code == 200:
            return redirect('ui_livres')
        else:
            print(f"ERREUR API (PUT): {response.text}")

    resp_livre = requests.get(url_livre)
    resp_auteurs = requests.get(f'{API_BASE_URL}/api/auteurs/')
    return render(request, 'modifier_livre.html', {
        'livre': resp_livre.json(),
        'auteurs': resp_auteurs.json()
    })

def liste_emprunts_ui(request):
    """Affiche la liste de tous les emprunts."""
    try:
        response = requests.get(EMPRUNTS_API_URL)
        emprunts = response.json() if response.status_code == 200 else []
    except:
        emprunts = []
    return render(request, 'emprunts.html', {'emprunts': emprunts})

@login_required(login_url='login')
def creer_emprunt_ui(request):
    if not request.user.is_staff:
        messages.error(request, "⚠️ Action interdite : Vous n'avez pas les droits d'administrateur.")
        return redirect('ui_emprunts')
    
    if request.method == 'POST':
        data = {
            "livre": request.POST.get('livre'),
            "nom_lecteur": request.POST.get('nom_lecteur'),
            "date_emprunt": request.POST.get('date_emprunt'),
            "date_retour": request.POST.get('date_retour'),
        }
        
        response = requests.post(EMPRUNTS_API_URL, json=data)
        
        if response.status_code == 201:
            messages.success(request, "Emprunt enregistré !")
            return redirect('ui_emprunts')
        else:
            print(f"ERREUR API: {response.text}")
            messages.error(request, f"Erreur : {response.text}")

    try:
        resp_livres = requests.get(LIVRES_API_URL)
        livres = resp_livres.json() if resp_livres.status_code == 200 else []
    except:
        livres = []
    
    return render(request, 'creer_emprunt.html', {'livres': livres})

@login_required(login_url='login')
def rendre_livre_ui(request, id):
    if not request.user.is_staff:
        messages.error(request, "⚠️ Action interdite : Vous n'avez pas les droits d'administrateur.")
        return redirect('ui_emprunts')
    
    requests.delete(f"{EMPRUNTS_API_URL}{id}/")
    return redirect('ui_emprunts')

def accueil(request):
    nb_visites = request.session.get('visites', 0) + 1
    request.session['visites'] = nb_visites
    return render(request, 'accueil.html', {'visites': nb_visites})