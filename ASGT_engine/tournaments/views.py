from django.http import HttpResponse
from django.shortcuts import render, redirect
from tournaments.models import Tournament, User, Games, Round1
from tournaments.forms import ContactUsForm, TournamentForm
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import random
import json

# l'object request est une convention et est un objet HttpRequest. Voir les méthodes sur la doc django




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
        # créer une instance de notre formulaire et le remplir avec les données POST
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
    game = Games.objects.get(game_name=tournament.game)

    return render(request, 'tournaments/tournament_detail.html', {'tournament': tournament, 'game': game})

@login_required
def tournament_create(request):
    i = 0
    if request.method == 'POST':
        tournament_form = TournamentForm(request.POST)
        round1_tournament = Round1()
        tournament_players = [tournament_form.player1, tournament_form.player2, tournament_form.player3, tournament_form.player4, tournament_form.player5, tournament_form.player6, tournament_form.player7, tournament_form.player8]

        #création d'une liste des joueurs 
        if tournament_form.is_valid():
            tournament_form = tournament_form.save()
            round_players = [round1_tournament.player1, round1_tournament.player2, round1_tournament.player3, round1_tournament.player4, round1_tournament.player5, round1_tournament.player6, round1_tournament.player7, round1_tournament.player8]

            #tant que la liste tournament_player n'est pas nulle, on ajoute en random les joueurs dans round_player
            while len(tournament_players) > 0:
                round_players[i] = random.choice(tournament_players)
                tournament_players.remove(round_players[i])
                i += 1
            round1_tournament.save()
            return redirect('tournament-detail', tournament_form.id)
    else:
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
