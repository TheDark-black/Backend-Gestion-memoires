from django.shortcuts import render
from django.http import JsonResponse
from backend.apps.users.models import Teacher, User

# Fonction pour afficher les enseignants inscrits
def get_registered_teachers():
    
    # retourne une liste de dictionnaires contenant les informations des enseignants

    # Ligne 1 : Récupérer tous les profils Teacher avec les infos utilisateur
    teachers = Teacher.objects.select_related('user').all()
    
    # Ligne 2 : Créer une liste vide pour stocker les données formatées
    registered_teachers_list = []
    
    # Ligne 3 : Boucler sur chaque enseignant trouvé
    for teacher in teachers:
        # Ligne 4 : Pour chaque enseignant, créer un dictionnaire avec ses infos
        teacher_data = {
            'id': str(teacher.id),  # Convertir l'UUID en texte
            'nom': teacher.user.nom, 
            'prenom': teacher.user.prenom,  
            'email': teacher.user.email, 
            'grade': teacher.grade, 
            'specialite': teacher.specialite, 
        }
        
        # Ligne 5 : Ajouter ce dictionnaire à notre liste
        registered_teachers_list.append(teacher_data)
    
    # Ligne 6 : Retourner la liste remplie
    return registered_teachers_list


# Vue Django pour afficher les enseignants inscrits 
def list_registered_teachers(request):
    
    # Cette vue retourne une réponse JSON avec tous les enseignants inscrits.
    # Elle peut être utilisée dans une URL pour afficher les données en API.
    teachers = get_registered_teachers()
    return JsonResponse({
        'success': True,
        'count': len(teachers),
        'data': teachers
    })
