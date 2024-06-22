# Import des modèles et des formulaires nécessaires
from tournaments.models import Tournament, User, Games, Round1, Round2, Round3
from tournaments.forms import ContactUsForm, TournamentForm, Round1Form, Round2Form, Round3Form

def save_scores_matchs(request, id):
    """
    Calcule les résultats des matchs pour les différents tours d'un tournoi.
    Cette fonction gère les sauvegardes en base de données des scores pour les tours 1, 2 et 3 d'un tournoi
    et met à jour les scores des joueurs dans les modèles Round1, Round2 et Round3 respectivement.
    
    Args:
        request: La requête HTTP contenant les données POST.
        id: L'identifiant du tournoi.

    Returns:
        Le formulaire du tour en cours avec les données validées ou non.
    """
    # Récupération des objets Round1, Round2 et Round3 liés au tournoi
    round1 = Round1.objects.get(tournament=id)
    round2 = Round2.objects.get(tournament=id)
    round3 = Round3.objects.get(tournament=id)
    i = 1  # Indice pour les scores des joueurs

    # Vérification si le tour 1 est ouvert pour enregistrement en base de données
    if round1.open == 'open':
        round1_form = Round1Form(request.POST)
        if round1_form.is_valid():
            cd = round1_form.cleaned_data
            # Parcourt les valeurs soumises et les attribue aux scores des joueurs
            for x in cd.values():
                setattr(round1, 'player{}_score'.format(i), x)
                i += 1
            round1.open = False  # Ferme le tour 1
            round1.save()
            define_next_round(id, 1)  # Définit les joueurs pour le prochain tour
        return round1_form
    # Vérification si le tour 2 est ouvert pour enregistrement en base de données
    if round2.open == 'open':
        round2_form = Round2Form(request.POST)
        if round2_form.is_valid():
            cd = round2_form.cleaned_data
            # Parcourt les valeurs soumises et les attribue aux scores des joueurs
            for x in cd.values():
                setattr(round2, 'player{}_score'.format(i), x)
                i += 1
            round2.open = False  # Ferme le tour 2
            round2.save()
    # Sinon, on considère que le tour 3 est ouvert pour pour enregistrement en base de données
    else:
        round3_form = Round3Form(request.POST)
        if round3_form.is_valid():
            cd = round3_form.cleaned_data
            # Parcourt les valeurs soumises et les attribue aux scores des joueurs
            for x in cd.values():
                setattr(round3, 'player{}_score'.format(i), x)
                i += 1
            round3.open = False  # Ferme le tour 3
            round3.save()

def define_next_round(id, round_nb):
    """
    Définit les joueurs pour le prochain tour en fonction des scores du tour précédent.
    
    Args:
        id: L'identifiant du tournoi.
        round_nb: Le numéro du tour actuel.

    Fonctionnement:
    - Pour le tour 1, on compare les scores des joueurs en paires (1 vs 2, 3 vs 4, etc.)
      et on attribue les gagnants au tour 2.
    - Pour le tour 2, on compare les scores des joueurs en paires (1 vs 2, 3 vs 4)
      et on attribue les gagnants au tour 3.
    """
    # Récupération des objets Round1, Round2 et Round3 liés au tournoi
    round1 = Round1.objects.get(tournament=id)
    round2 = Round2.objects.get(tournament=id)
    round3 = Round3.objects.get(tournament=id)

    # Définition des gagnants pour le prochain tour en fonction du tour actuel
    match round_nb:
        case 1:
            # Pour le tour 1, on détermine les gagnants pour le tour 2
            for i in range(1, 8, 2):
                if getattr(round1, f"player{i}_score") > getattr(round1, f"player{i+1}_score"):
                    setattr(round2, f"player{i}", getattr(round1, f"player{i}"))
                else:
                    setattr(round2, f"player{i+1}", getattr(round1, f"player{i+1}"))
            round2.save()
        case 2:
            # Pour le tour 2, on détermine les gagnants pour le tour 3
            for i in range(1, 4, 2):
                if getattr(round2, f"player{i}_score") > getattr(round2, f"player{i+1}_score"):
                    setattr(round3, f"player{i}", getattr(round2, f"player{i}"))
                else:
                    setattr(round3, f"player{i+1}", getattr(round2, f"player{i+1}"))
            round3.save()
