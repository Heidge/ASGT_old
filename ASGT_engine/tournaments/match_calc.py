from tournaments.models import Tournament, User, Games, Round1, Round2, Round3
from tournaments.forms import ContactUsForm, TournamentForm, Round1Form, Round2Form, Round3Form
    


def match_calc(request, id):
    round1 = Round1.objects.get(tournament=id)
    round2 = Round2.objects.get(tournament=id)
    round3 = Round3.objects.get(tournament=id)
    i = 1

    if (round1.open == 'open'):
        round1_form = Round1Form(request.POST)
        if round1_form.is_valid():
            cd = round1_form.cleaned_data
            for x in cd.values():
                setattr(round1, 'player{}_score'.format(i), x)
                i += 1
            round1.open = False
            round1.save()
            define_next(id, 1)
        return round1_form
    elif (round2.open == 'open'):
        round2_form = Round2Form(request.POST)
        if round2_form.is_valid():
            cd = round2_form.cleaned_data
            for x in cd.values():
                setattr(round2, 'player{}_score'.format(i), x)
                i += 1
            round2.open = False
            round2.save()
    else:
        round3_form = Round3Form(request.POST)
        if round3_form.is_valid():
            cd = round3_form.cleaned_data
            for x in cd.values():
                setattr(round3, 'player{}_score'.format(i), x)
                i += 1
            round3.open = False
            round3.save()
    

def define_next(id, round_nb):
    round1 = Round1.objects.get(tournament=id)
    round2 = Round2.objects.get(tournament=id)
    round3 = Round3.objects.get(tournament=id)
    match round_nb:
        case 1:
            for i in range(1,8,2):
                if getattr(round1, f"player{i}_score") > getattr(round1, f"player{i+1}_score"):
                    setattr(round2, f"player{i}", getattr(round1, f"player{i}"))
                else:
                    setattr(round2, f"player{i+1}", getattr(round1, f"player{i+1}"))
            round2.save()
        case 2:
            for i in range(1,4,2):
                if getattr(round2, f"player{i}_score") > getattr(round2, f"player{i+1}_score"):
                    setattr(round3, f"player{i}", getattr(round2, f"player{i}"))
                else:
                    setattr(round3, f"player{i+1}", getattr(round2, f"player{i+1}"))
            round3.save()
        




    

