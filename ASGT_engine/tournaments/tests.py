from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from .models import User, Games, Tournament, Round1, Round2, Round3

class ModelsTestCase(TestCase):
    def setUp(self):
        self.game = Games.objects.create(game_name='Test Game', game_description='A test game')

    def test_user_username_type(self):
        with self.assertRaises(ValidationError):
            # Essayer de créer un utilisateur avec un username de type integer
            User.objects.create(username=123, email='test@example.com', password='securepassword')

    def test_user_email_required(self):
        with self.assertRaises(ValidationError):
            # Essayer de créer un utilisateur sans email
            User.objects.create(username='testuser', password='securepassword')

    def test_games_game_name_required(self):
        with self.assertRaises(ValidationError):
            # Essayer de créer un jeu sans nom de jeu
            Games.objects.create(game_description='A test game')

    def test_tournament_nb_players_type(self):
        with self.assertRaises(ValidationError):
            # Essayer de créer un tournoi avec nb_players de type str au lieu de int
            Tournament.objects.create(
                tournament_name='Test Tournament',
                game=self.game,
                admin=None,
                start_date=timezone.now().date(),
                start_time=timezone.now().time(),
                nb_players='8',  # C'est une chaîne de caractères au lieu d'un entier
                player1='Player 1',
                player2='Player 2',
                player3='Player 3',
                player4='Player 4',
                player5='Player 5',
                player6='Player 6',
                player7='Player 7',
                player8='Player 8'
            )

    def test_tournament_players_required(self):
        with self.assertRaises(ValidationError):
            # Essayer de créer un tournoi sans spécifier tous les joueurs
            Tournament.objects.create(
                tournament_name='Test Tournament',
                game=self.game,
                admin=None,
                start_date=timezone.now().date(),
                start_time=timezone.now().time(),
                nb_players=8,
                player1='Player 1',
                player2='Player 2'
                # Les autres joueurs manquants
            )

    def test_round_player_score_type(self):
        tournament = Tournament.objects.create(
            tournament_name='Test Tournament',
            game=self.game,
            admin=None,
            start_date=timezone.now().date(),
            start_time=timezone.now().time(),
            nb_players=8,
            player1='Player 1',
            player2='Player 2',
            player3='Player 3',
            player4='Player 4',
            player5='Player 5',
            player6='Player 6',
            player7='Player 7',
            player8='Player 8'
        )
        with self.assertRaises(ValidationError):
            # Essayer de créer un round avec player1_score de type str au lieu de int
            Round1.objects.create(
                tournament=tournament,
                player1='Player 1',
                player2='Player 2',
                player3='Player 3',
                player4='Player 4',
                player5='Player 5',
                player6='Player 6',
                player7='Player 7',
                player8='Player 8',
                player1_score='10',  # C'est une chaîne de caractères au lieu d'un entier
                player2_score=3,
                player3_score=2,
                player4_score=8,
                player5_score=4,
                player6_score=5,
                player7_score=1,
                player8_score=3,
                open=True
            )

    def test_round_player_name_type(self):
        tournament = Tournament.objects.create(
            tournament_name='Test Tournament',
            game=self.game,
            admin=None,
            start_date=timezone.now().date(),
            start_time=timezone.now().time(),
            nb_players=8,
            player1='Player 1',
            player2='Player 2',
            player3='Player 3',
            player4='Player 4',
            player5='Player 5',
            player6='Player 6',
            player7='Player 7',
            player8='Player 8'
        )
        with self.assertRaises(ValidationError):
            # Essayer de créer un round avec player1 de type int au lieu de str
            Round1.objects.create(
                tournament=tournament,
                player1=1,  # C'est un entier au lieu d'une chaîne de caractères
                player2='Player 2',
                player3='Player 3',
                player4='Player 4',
                player5='Player 5',
                player6='Player 6',
                player7='Player 7',
                player8='Player 8',
                player1_score=0,
                player2_score=0,
                player3_score=0,
                player4_score=0,
                player5_score=0,
                player6_score=0,
                player7_score=0,
                player8_score=0,
                open=True
            )

    def test_round_duplicate_players(self):
        tournament = Tournament.objects.create(
            tournament_name='Test Tournament',
            game=self.game,
            admin=None,
            start_date=timezone.now().date(),
            start_time=timezone.now().time(),
            nb_players=8,
            player1='Player 1',
            player2='Player 2',
            player3='Player 3',
            player4='Player 4',
            player5='Player 5',
            player6='Player 6',
            player7='Player 7',
            player8='Player 8'
        )
        with self.assertRaises(ValidationError):
            # Essayer de créer un round avec des joueurs dupliqués
            Round1.objects.create(
                tournament=tournament,
                player1='Player 1',
                player2='Player 1',  # Player 1 est dupliqué
                player3='Player 3',
                player4='Player 4',
                player5='Player 5',
                player6='Player 6',
                player7='Player 7',
                player8='Player 8',
                player1_score=4,
                player2_score=3,
                player3_score=2,
                player4_score=8,
                player5_score=4,
                player6_score=5,
                player7_score=1,
                player8_score=3,
                open=True
            )

    def test_round_invalid_scores(self):
        tournament = Tournament.objects.create(
            tournament_name='Test Tournament',
            game=self.game,
            admin=None,
            start_date=timezone.now().date(),
            start_time=timezone.now().time(),
            nb_players=8,
            player1='Player 1',
            player2='Player 2',
            player3='Player 3',
            player4='Player 4',
            player5='Player 5',
            player6='Player 6',
            player7='Player 7',
            player8='Player 8'
        )
        with self.assertRaises(ValidationError):
            # Essayer de créer un round avec des scores invalides (négatifs)
            Round1.objects.create(
                tournament=tournament,
                player1='Player 1',
                player2='Player 2',
                player3='Player 3',
                player4='Player 4',
                player5='Player 5',
                player6='Player 6',
                player7='Player 7',
                player8='Player 8',
                player1_score=-1,  # Score négatif
                player2_score=0,
                player3_score=0,
                player4_score=0,
                player5_score=0,
                player6_score=0,
                player7_score=0,
                player8_score=0,
                open=True
            )
