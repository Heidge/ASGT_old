from django.http import HttpResponse
from django.shortcuts import render, redirect
from tournaments.models import Tournament, User, Games, Round1, Round2, Round3
from tournaments.forms import ContactUsForm, TournamentForm, Round1Form
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from tournaments import match_calc
import random
import json


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
    game = Games.objects.get(game_name=tournament.game)
    
    if request.method == 'POST':
        round_form = match_calc.match_calc(request, tournament_id)
    else:
        round_form = Round1Form()

    return render(request, 'tournaments/tournament_detail.html', {'tournament': tournament, 'game': game, 'round1': round1, 'round1_form': round_form})

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

        # Crée des instances pour les trois rounds du tournoi
        round1_tournament = Round1()
        round2_tournament = Round2()
        round3_tournament = Round3()

        if tournament_form.is_valid():
            # Récupère les données nettoyées du formulaire
            tournament_infos = tournament_form.cleaned_data

            # Sauvegarde le formulaire et lie les rounds au tournoi
            tournament_form = tournament_form.save()
            round1_tournament.tournament = tournament_form
            round2_tournament.tournament = tournament_form
            round3_tournament.tournament = tournament_form

            # Sauvegarde les rounds dans la base de données
            round2_tournament.save()
            round3_tournament.save()

            # Récupère la liste des joueurs du formulaire
            players_from_form = ['player1', 'player2', 'player3', 'player4', 'player5', 'player6', 'player7', 'player8']
            tournament_players = [tournament_infos[player] for player in players_from_form]

            # Initialise la liste des joueurs pour les rounds
            round_players = [getattr(round1_tournament, player) for player in players_from_form]

            # Attribue les joueurs aux rounds jusqu'à épuisement de la liste des joueurs disponibles
            while len(tournament_players) > 0:
                round_players[i] = random.choice(tournament_players)
                tournament_players.remove(round_players[i])
                setattr(round1_tournament, 'player{}'.format(i + 1), round_players[i])
                i += 1     

            # Sauvegarde le premier round avec les joueurs attribués
            round1_tournament.save()

            # Redirige vers la page de détail du tournoi créé
            return redirect('tournament-detail', tournament_form.id)
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
