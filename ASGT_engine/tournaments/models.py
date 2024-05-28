from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

# Si nous souhaitez créer un objet (ou un champ) dans une BDD, toujours faire hériter de models.Model
# tournaments/models.py

class User(models.Model):

    def __str__(self):
        return f'{self.username}' #permet d'afficher directement le username dans l'administration Django plutôt qu'un nom d'objet + id

    username = models.fields.CharField(max_length=30)
    created_at = models.fields.DateTimeField(
        default=timezone.now(),
        verbose_name='Créé le'
        )
    updated_at = models.fields.DateTimeField(
        auto_now=True,
        verbose_name='Modifié le'
        )
    email = models.fields.EmailField(
        blank=False,
        null=True
        )
    password = models.fields.CharField(
        max_length=25,
        blank=False,
        null=True
        )

class Games(models.Model):

    def __str__(self):
        return f'{self.game_name}'

    game_name = models.fields.CharField(max_length=100)
    created_at = models.fields.DateTimeField(
        default=timezone.now(),
        verbose_name = 'Ajouté le'
        )
    game_description = models.fields.TextField(max_length=1000)

    game_image = models.ImageField(upload_to='games/', blank=True, null=True)

class Tournament(models.Model):

    def __str__(self):
        return f'{self.tournament_name}'


    tournament_name = models.fields.CharField(
        max_length=100,
        verbose_name="Nom du tournoi",
        blank=False,
        null=True
        )
    
    created_at = models.fields.DateTimeField(
        default=timezone.now(),
        verbose_name="Créé le"
        )
    
    updated_at = models.fields.DateTimeField(auto_now=True)

    nb_players = models.fields.IntegerField(validators=
        [MinValueValidator(8, "Le nombre de participants est imposé à 8 pour le moment"),
        MaxValueValidator(8, "Le nombre de participants est imposé à 8 pour le moment")],
        verbose_name="Nombre de participants",
        blank=False,
        null=True
        )
    
    game = models.ForeignKey(
        Games,
        on_delete=models.SET_NULL,
        verbose_name='Jeu',
        blank=False,
        null=True
        )
    
    admin = models.ForeignKey(
        User,
        null=True,
        on_delete=models.SET_NULL, #set_null car si on utilise CASCADE ça supprimera tout le tournoi
        verbose_name="Propriétaire",
        related_name='+'
        )
    
    player1 = models.fields.CharField(
        max_length=20,
        verbose_name="Joueur 1",
        blank=False,
        null=True)
    
    player2 = models.fields.CharField(
        max_length=20,
        verbose_name="Joueur 2",
        blank=False,
        null=True)
    
    player3 = models.fields.CharField(
        max_length=20,
        verbose_name="Joueur 3",
        blank=False,
        null=True)
    
    player4 = models.fields.CharField(
        max_length=20,
        verbose_name="Joueur 4",
        blank=False,
        null=True)
    
    player5 = models.fields.CharField(
        max_length=20,
        verbose_name="Joueur 5",
        blank=False,
        null=True)
    
    player6 = models.fields.CharField(
        max_length=20,
        verbose_name="Joueur 6",
        blank=False,
        null=True)
    
    player7 = models.fields.CharField(
        max_length=20,
        verbose_name="Joueur 7",
        blank=False,
        null=True)
    
    player8 = models.fields.CharField(
        max_length=20,
        verbose_name="Joueur 8",
        blank=False,
        null=True)
    
    start_date = models.fields.DateField(
        verbose_name="Date de début",
        blank=False,
        null=True
        )
    
    start_time = models.fields.TimeField(
        verbose_name="Heure de début",
        blank=False,
        null=True
        )

class Round1(models.Model):

    def __str__(self):
        return f'{self.tournament}'

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.SET_NULL,
        verbose_name="Tournoi",
        blank=False,
        null=True
    )
    
    created_at = models.fields.DateTimeField(
        default=timezone.now(),
        verbose_name="Créé le"
        )
    
    updated_at = models.fields.DateTimeField(auto_now=True)
    
    player1 = models.fields.CharField(
        max_length=20,
        verbose_name="Joueur 1",
        blank=False,
        null=True)
    
    player1_score = models.fields.IntegerField(
        verbose_name="Score joueur 1",
        blank=False,
        null=True)
    
    player2 = models.fields.CharField(
        max_length=20,
        verbose_name="Joueur 2",
        blank=False,
        null=True)
    
    player2_score = models.fields.IntegerField(
        verbose_name="Score joueur 2",
        blank=False,
        null=True)

    player3 = models.fields.CharField(
        max_length=20,
        verbose_name="Joueur 3",
        blank=False,
        null=True)
    
    player3_score = models.fields.IntegerField(
        verbose_name="Score joueur 3",
        blank=False,
        null=True)

    player4 = models.fields.CharField(
        max_length=20,
        verbose_name="Joueur 4",
        blank=False,
        null=True)
    
    player4_score = models.fields.IntegerField(
        verbose_name="Score joueur 4",
        blank=False,
        null=True)

    player5 = models.fields.CharField(
        max_length=20,
        verbose_name="Joueur 5",
        blank=False,
        null=True)
    
    player5_score = models.fields.IntegerField(
        verbose_name="Score joueur 5",
        blank=False,
        null=True)

    player6 = models.fields.CharField(
        max_length=20,
        verbose_name="Joueur 6",
        blank=False,
        null=True)
    
    player6_score = models.fields.IntegerField(
        verbose_name="Score joueur 6",
        blank=False,
        null=True)

    player7 = models.fields.CharField(
        max_length=20,
        verbose_name="Joueur 7",
        blank=False,
        null=True)
    
    player7_score = models.fields.IntegerField(
        verbose_name="Score joueur 7",
        blank=False,
        null=True)

    player8 = models.fields.CharField(
        max_length=20,
        verbose_name="Joueur 8",
        blank=False,
        null=True)

    player8_score = models.fields.IntegerField(
        verbose_name="Score joueur 8",
        blank=False,
        null=True)
    
    open = models.fields.BooleanField(
        verbose_name="Round ouvert",
        blank=False,
        default=True
    )

class Round2(models.Model):

    def __str__(self):
        return str(self.id)

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.SET_NULL,
        verbose_name="Tournoi",
        blank=False,
        null=True
    )
    
    created_at = models.fields.DateTimeField(
        default=timezone.now(),
        verbose_name="Créé le"
        )
    
    updated_at = models.fields.DateTimeField(auto_now=True)
    
    player1 = models.fields.CharField(
        max_length=20,
        verbose_name="Joueur 1",
        blank=False,
        null=True)
    
    player1_score = models.fields.IntegerField(
        verbose_name="Score joueur 1",
        blank=False,
        null=True)
    
    player2 = models.fields.CharField(
        max_length=20,
        verbose_name="Joueur 2",
        blank=False,
        null=True)
    
    player2_score = models.fields.IntegerField(
        verbose_name="Score joueur 2",
        blank=False,
        null=True)

    player3 = models.fields.CharField(
        max_length=20,
        verbose_name="Joueur 3",
        blank=False,
        null=True)
    
    player3_score = models.fields.IntegerField(
        verbose_name="Score joueur 3",
        blank=False,
        null=True)

    player4 = models.fields.CharField(
        max_length=20,
        verbose_name="Joueur 4",
        blank=False,
        null=True)
    
    player4_score = models.fields.IntegerField(
        verbose_name="Score joueur 4",
        blank=False,
        null=True)
    
    open = models.fields.BooleanField(
        verbose_name="Round ouvert",
        blank=False,
        default=True
    )
    
class Round3(models.Model):

    def __str__(self):
        return str(self.id)

    tournament = models.ForeignKey(
        Tournament,
        on_delete=models.SET_NULL,
        verbose_name="Tournoi",
        blank=False,
        null=True
    )
    
    created_at = models.fields.DateTimeField(
        default=timezone.now(),
        verbose_name="Créé le"
        )
    
    updated_at = models.fields.DateTimeField(auto_now=True)
    
    player1 = models.fields.CharField(
        max_length=20,
        verbose_name="Joueur 1",
        blank=False,
        null=True)
    
    player1_score = models.fields.IntegerField(
        verbose_name="Score joueur 1",
        blank=False,
        null=True)
    
    player2 = models.fields.CharField(
        max_length=20,
        verbose_name="Joueur 2",
        blank=False,
        null=True)
    
    player2_score = models.fields.IntegerField(
        verbose_name="Score joueur 2",
        blank=False,
        null=True)
    
    open = models.fields.BooleanField(
        verbose_name="Round ouvert",
        blank=False,
        default=True
    )
