# Import des modèles et des formulaires nécessaires
from tournaments.models import Tournament, User, Games, Round1, Round2, Round3
from tournaments.forms import ContactUsForm, TournamentForm, Round1Form, Round2Form, Round3Form
import logging
logger = logging.getLogger(__name__)

def save_scores_matchs(request, id):
    round1 = Round1.objects.get(tournament=id)
    round2 = Round2.objects.get(tournament=id)
    round3 = Round3.objects.get(tournament=id)
    i = 1

    if round1.open:
        round1_form = Round1Form(request.POST)
        if round1_form.is_valid():
            cd = round1_form.cleaned_data
            for x in cd.values():
                setattr(round1, 'player{}_score'.format(i), x)
                i += 1
            round1.open = False
            round1.save()
            define_next_round(id, 1)
        return round1_form
    elif round2.open:
        round2_form = Round2Form(request.POST)
        if round2_form.is_valid():
            cd = round2_form.cleaned_data
            i = 1
            for x in cd.values():
                setattr(round2, 'player{}_score'.format(i), x)
                i += 1
            round2.open = False
            round2.save()
            define_next_round(id, 2)
        return round2_form
    else:
        round3_form = Round3Form(request.POST)
        if round3_form.is_valid():
            cd = round3_form.cleaned_data
            i = 1
            for x in cd.values():
                setattr(round3, 'player{}_score'.format(i), x)
                i += 1
            round3.open = False
            round3.save()
        return round3_form

def define_next_round(id, round_nb):
    """
    Définit les joueurs pour le prochain tour en fonction des scores du tour précédent.
    
    Args:
        id: L'identifiant du tournoi.
        round_nb: Le numéro du tour actuel (1 pour round1, 2 pour round2, etc.).

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
    if round_nb == 1:
        # Pour le tour 1, on compare les scores de round1 et attribue les gagnants à round2
        for i in range(1, 8 // 2 + 1):
            j = (i - 1) * 2 + 1  # Calculer l'index correct pour les paires de joueurs
            player1_score = getattr(round1, f"player{j}_score", 0)
            player2_score = getattr(round1, f"player{j+1}_score", 0)

            if player1_score > player2_score:
                setattr(round2, f"player{i}", getattr(round1, f"player{j}"))
            else:
                setattr(round2, f"player{i}", getattr(round1, f"player{j+1}"))

        # Sauvegarde de round2 seulement si des modifications ont été faites
        round2.save()

    elif round_nb == 2:
        # Pour le tour 2, on compare les scores de round2 et attribue les gagnants à round3
        for i in range(1, 4 // 2 + 1):
            j = (i - 1) * 2 + 1  # Calculer l'index correct pour les paires de joueurs
            player1_score = getattr(round2, f"player{j}_score", 0)
            player2_score = getattr(round2, f"player{j+1}_score", 0)

            if player1_score > player2_score:
                setattr(round3, f"player{i}", getattr(round2, f"player{j}"))
            else:
                setattr(round3, f"player{i}", getattr(round2, f"player{j+1}"))

        # Sauvegarde de round3 seulement si des modifications ont été faites
        round3.save()
