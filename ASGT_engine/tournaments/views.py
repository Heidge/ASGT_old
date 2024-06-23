from django.http import HttpResponse
from django.shortcuts import render, redirect
from tournaments.models import Tournament, User, Games, Round1, Round2, Round3
from tournaments.forms import ContactUsForm, TournamentForm, Round1Form, Round2Form, Round3Form
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from tournaments import match_calc
import random
import json
import logging
logger = logging.getLogger(__name__)


def homepage(request):
    user = User.objects.all()
    return render(request, 'tournaments/homepage.html', {'users': user})

def games(request):
    games = Games.objects.all()
    return render(request, 'tournaments/games.html', {'games': games})

def about(request):
    return render(request, 'tournaments/about-us.html')

def tournament(request):
    tournaments = Tournament.objects.all()

    tg = {}
    for tournament in tournaments:
        tg[tournament.tournament_name] = tournament.game

    game_image = {}
    for tournament, game in tg.items():
        game_image[tournament] = game.game_image


    return render(request, 'tournaments/tournaments.html', {'tournaments': tournaments, 'game_image': game_image})

def contact(request):

    if request.method == 'POST':
        form = ContactUsForm(request.POST)

        if form.is_valid():
            send_mail(
            subject=f'Message de {form.cleaned_data["name"]} d\'ASGT - formulaire de contact',
            message=form.cleaned_data['message'],
            from_email=form.cleaned_data['email'],
            recipient_list=['axel.gore@outlook.fr']
        )
        return redirect('/confirmation-contact')
    else:
        form = ContactUsForm()

    return render(request, 'tournaments/contact.html', {'form': form})

def contact_ok(request):
    return render(request, 'tournaments/contact-ok.html')

def tournament_detail(request, tournament_id):
    tournament = Tournament.objects.get(id=tournament_id)
    round1 = Round1.objects.get(tournament=tournament_id)
    round2 = Round2.objects.get(tournament=tournament_id)
    round3 = Round3.objects.get(tournament=tournament_id)
    game = Games.objects.get(game_name=tournament.game)
    round1_form = Round1Form()
    round2_form = Round2Form()
    round3_form = Round3Form()
    
    if request.method == 'POST':
        
        if round1.open:
            round1_form = Round1Form(request.POST)
            if round1_form.is_valid():
                match_calc.save_scores_matchs(request, tournament_id)
                round1 = Round1.objects.get(tournament=tournament_id)
                round2 = Round2.objects.get(tournament=tournament_id)
                round3 = Round3.objects.get(tournament=tournament_id)
        elif round2.open:
            round2_form = Round2Form(request.POST)
            if round2_form.is_valid():
                print("ok")
                match_calc.save_scores_matchs(request, tournament_id)
                round1 = Round1.objects.get(tournament=tournament_id)
                round2 = Round2.objects.get(tournament=tournament_id)
                round3 = Round3.objects.get(tournament=tournament_id)
            else:
                print(round2_form.errors)
        else:
            round3_form = Round3Form(request.POST)
            if round3_form.is_valid():
                match_calc.save_scores_matchs(request, tournament_id)
                round1 = Round1.objects.get(tournament=tournament_id)
                round2 = Round2.objects.get(tournament=tournament_id)
                round3 = Round3.objects.get(tournament=tournament_id)

    return render(request, 'tournaments/tournament_detail.html', {'tournament': tournament, 'game': game, 'round1': round1, 'round1_form': round1_form, 'round2': round2, 'round2_form': round2_form, 'round3': round3, 'round3_form': round3_form})

@login_required
def tournament_create(request):
    """
    Crée un nouveau tournoi et attribue les joueurs aux tours.

    Cette fonction permet à un utilisateur authentifié de créer un nouveau tournoi,
    de sélectionner les joueurs pour chaque tour et de sauvegarder ces informations
    dans la base de données.

    Args:
        request (HttpRequest): L'objet HttpRequest contenant les données envoyées par l'utilisateur.

    Returns:
        HttpResponse: Redirige vers la page de détail du tournoi créé ou renvoie le formulaire
                      de création de tournoi si la requête n'est pas une requête POST.
    """

    i = 0  # Compteur pour attribuer les joueurs aux tours

    if request.method == 'POST':
        # Initialise le formulaire de création de tournoi avec les données POST
        tournament_form = TournamentForm(request.POST)

        if tournament_form.is_valid():
            # Récupère les données nettoyées du formulaire
            tournament_infos = tournament_form.cleaned_data

            # Sauvegarde le tournoi
            tournament = tournament_form.save()

            # Crée des instances pour les trois rounds du tournoi
            round1_tournament = Round1(tournament=tournament)
            round2_tournament = Round2(tournament=tournament)
            round3_tournament = Round3(tournament=tournament)

            # Sauvegarde les rounds dans la base de données
            round1_tournament.save()
            round2_tournament.save()
            round3_tournament.save()

            # Récupère la liste des joueurs du formulaire
            players_from_form = ['player1', 'player2', 'player3', 'player4', 'player5', 'player6', 'player7', 'player8']
            tournament_players = [tournament_infos[player] for player in players_from_form]

            # Attribue les joueurs aux rounds jusqu'à épuisement de la liste des joueurs disponibles
            for player_attr in players_from_form:
                if tournament_players:
                    selected_player = random.choice(tournament_players)
                    tournament_players.remove(selected_player)
                    setattr(round1_tournament, player_attr, selected_player)
                    round1_tournament.save()

            # Redirige vers la page de détail du tournoi créé
            return redirect('tournament-detail', tournament.id)
    else:
        # Si la requête n'est pas une requête POST, initialise le formulaire vide
        tournament_form = TournamentForm()

    return render(request, 'tournaments/tournament-creation.html', {'form': tournament_form})

def tournament_update(request, tournament_id):

    tournament = Tournament.objects.get(id=tournament_id)

    if request.method == 'POST':
        tournament_form = TournamentForm(request.POST, instance=tournament)
        if tournament_form.is_valid():
            tournament_form.save()
            return redirect('tournament-detail', tournament.id)
    else:
        tournament_form = TournamentForm(instance=tournament)
    return render(request, 'tournaments/tournament-update.html', {'tournament_form': tournament_form})

def tournament_delete(request, tournament_id):
        tournament = Tournament.objects.get(id=tournament_id)

        if request.method == 'POST':
            tournament.delete()
            return redirect('tournament-list')

        return render(request, 'tournaments/tournament_delete.html', {'tournament': tournament})
