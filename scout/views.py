from django.shortcuts import render
from django.http import HttpResponse, request
from django_tables2 import RequestConfig
from django.views.generic import DetailView, FormView, CreateView, UpdateView, ListView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Team, Robot, MatchResult
from .tables import TeamTable, MatchResultTable

from . import utils

# Create your views here.
def public_view(request):
    # return HttpResponse("Public View")
    return render(request, 'scout/base.html')


def teams(request):
    table = TeamTable(Team.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'scout/teams.html', {'table': table})




def team_summary(request, number):
    try:
        team = Team.objects.get(number=number)
    except Team.DoesNotExist:
        return HttpResponse("Team {} not found.".format(number))

    return render(request, 'scout/team_summary.html', {'team': team})


class RobotCreateView(LoginRequiredMixin, CreateView):
    model = Robot
    fields = "__all__"


class MatchCreateView(LoginRequiredMixin, CreateView):
    model = MatchResult
    fields = "__all__"


class MatchResultListView(ListView):
    model = MatchResult
    fields = "__all__"
    # queryset = MatchResult.objects.all()
    # queryset = MatchResult.objects.order_by('match_number')

    context_object_name = "match_result_list"


def matches(request):
    table = MatchResultTable(MatchResult.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'scout/teams.html', {'table': table})


def qualifier_predictor(request, number):
    match = utils.get_qualifier_match(number)

    if match == None:
        return HttpResponse(f"No information found for match: {number}") 

    # We the match
    teams = {}
    match_score = {'auto_points': '2', 'teleop_points': '10', 'endgame_points': '15'}

    team1 = {'number' : match['alliances']['red']['team_keys'][0],
             'auto_points' : match_score['auto_points'],
             'teleop_points' : match_score['teleop_points'],
             'endgame_points' : match_score['endgame_points']

    }
    team2 = {'number' : match['alliances']['red']['team_keys'][1],
             'auto_points' : match_score['auto_points'],
             'teleop_points' : match_score['teleop_points'],
             'endgame_points' : match_score['endgame_points']

    }
    team3 = {'number' : match['alliances']['red']['team_keys'][2],
             'auto_points' : match_score['auto_points'],
             'teleop_points' : match_score['teleop_points'],
             'endgame_points' : match_score['endgame_points']

    }
    team4 = {'number' : match['alliances']['red']['team_keys'][0],
             'auto_points' : match_score['auto_points'],
             'teleop_points' : match_score['teleop_points'],
             'endgame_points' : match_score['endgame_points']

    }
    team5 = {'number' : match['alliances']['red']['team_keys'][1],
             'auto_points' : match_score['auto_points'],
             'teleop_points' : match_score['teleop_points'],
             'endgame_points' : match_score['endgame_points']

    }
    team6 = {'number' : match['alliances']['red']['team_keys'][2],
             'auto_points' : match_score['auto_points'],
             'teleop_points' : match_score['teleop_points'],
             'endgame_points' : match_score['endgame_points']

    }
 
    

    teams['r1'] = team1
    teams['r2'] = team2
    teams['r3'] = team3
    teams['b1'] = team4
    teams['b2'] = team5
    teams['b3'] = team6

    # RequestConfig(request).configure(teams)
    return render(request, 'scout/predictor_table.html', {'teams': teams})


    


    