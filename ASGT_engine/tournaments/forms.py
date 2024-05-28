from django import forms
from tournaments.models import Tournament, Games, Round1, Round2, Round3

class ContactUsForm(forms.Form):

    name = forms.CharField(
        label='Nom',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Votre nom',
        })
    )
    email = forms.EmailField(
        label='Adresse email',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Votre adresse email',
        })
    )
    message = forms.CharField(
        label='Message',
        max_length=500,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Entrez votre message ici',
        })
    )
class TournamentForm(forms.ModelForm):

    class Meta:
        model = Tournament
        fields = ['tournament_name', 'nb_players', 'game',
                  'player1', 'player2', 'player3', 'player4',
                  'player5', 'player6', 'player7', 'player8',
                  'start_date', 'start_time']

    tournament_name = forms.CharField(
        label='Nom du tournoi',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Entrez le nom du tournoi',
        })
    )
    nb_players = forms.IntegerField(
        label='Nombre de joueurs',
        required=True,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Entrez le nombre de joueurs (8)',
            'min': 8,
            'max': 8,
        })
    )
    game = forms.ModelChoiceField(
        label='Jeu',
        queryset=Games.objects.all(),
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control form-control-sm',
        })
    )
    player1 = forms.CharField(
        label='Joueur 1',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Entrez le nom du joueur 1',
        })
    )
    player2 = forms.CharField(
        label='Joueur 2',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Entrez le nom du joueur 2',
        })
    )
    player3 = forms.CharField(
        label='Joueur 3',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Entrez le nom du joueur 3',
        })
    )
    player4 = forms.CharField(
        label='Joueur 4',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Entrez le nom du joueur 4',
        })
    )
    player5 = forms.CharField(
        label='Joueur 5',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Entrez le nom du joueur 5',
        })
    )
    player6 = forms.CharField(
        label='Joueur 6',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Entrez le nom du joueur 6',
        })
    )
    player7 = forms.CharField(
        label='Joueur 7',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Entrez le nom du joueur 7',
        })
    )
    player8 = forms.CharField(
        label='Joueur 8',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Entrez le nom du joueur 8',
        })
    )
    start_date = forms.DateField(
        label='Date de début',
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Entrez la date de début',
            'type': 'date',
        })
    )

    start_time = forms.TimeField(
        label='Heure de début',
        required=True,
        widget=forms.TimeInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Entrez l\'heure de début',
            'type': 'time',
        })
    )

class Round1Form(forms.ModelForm):
    class Meta:
        model = Round1
        fields = ['player1_score', 'player2_score', 'player3_score', 'player4_score',
                  'player5_score', 'player6_score', 'player7_score', 'player8_score',
                  ]


    player1_score = forms.IntegerField(
        label='Score J1',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm'
        })
    )
    player2_score = forms.IntegerField(
        label='Score J2',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm'
        })
    )
    player3_score = forms.IntegerField(
        label='Score J3',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm'
        })
    )
    player4_score = forms.IntegerField(
        label='Score J4',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm'
        })
    )
    player5_score = forms.IntegerField(
        label='Score J5',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm'
        })
    )
    player6_score = forms.IntegerField(
        label='Score J6',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm'
        })
    )
    player7_score = forms.IntegerField(
        label='Score J7',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm'
        })
    )
    player8_score = forms.IntegerField(
        label='Score J8',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm'
        })
    )

class Round2Form(forms.ModelForm):
    class Meta:
        model = Round2
        fields = ['player1_score', 'player2_score', 'player3_score', 'player4_score']


    player1_score = forms.IntegerField(
        label='Score J1',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm'
        })
    )
    player2_score = forms.IntegerField(
        label='Score J2',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm'
        })
    )
    player3_score = forms.IntegerField(
        label='Score J3',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm'
        })
    )
    player4_score = forms.IntegerField(
        label='Score J4',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm'
        })
    )

class Round3Form(forms.ModelForm):
    class Meta:
        model = Round3
        fields = ['player1_score', 'player2_score']

    player1_score = forms.IntegerField(
        label='Score J1',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm'
        })
    )
    
    player2_score = forms.IntegerField(
        label='Score J2',
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm'
        })
    )
