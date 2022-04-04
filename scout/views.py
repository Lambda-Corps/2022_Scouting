from django.shortcuts import render
from django.http import HttpResponse, request
from django_tables2 import RequestConfig
from django.views.generic import DetailView, FormView, CreateView, UpdateView, ListView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

import urllib3
import certifi
import json

from .models import Team, Robot, MatchResult
from .tables import TeamTable, MatchResultTable

# Create your views here.
def public_view(request):
    # return HttpResponse("Public View")
    return render(request, 'scout/base.html')


def teams(request):
    table = TeamTable(Team.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'scout/teams.html', {'table': table})

@login_required
def update_event():
    url = "https://www.thebluealliance.com/api/v3/event/2022chcmp/teams/simple"
    accept_header = 'application/json'
    auth_key = 'BJG4S2d2nkSkXikztbXHWBL8riwfb4ghAhUIXJ5dezxxhBpvC8ngqrekG2kjF5JV'
    headers = {
        'accept' : 'application/json',
        'X-TBA-Auth-Key' : auth_key,
        'User-Agent' : '1895_Scouter'
    }

    http = urllib3.PoolManager(ca_certs=certifi.where())
    req = http.request('GET', url, headers)

    teams = json.loads(req.data.decode('UTF-8'))

    for team in teams:
        Team.objects.create(name=team['nickname'], number=team['team_number'], frc_key=team['key'])

    # Team.save()

    return HttpResponse(teams)

@login_required
def update_event_json():
    teams = {}
    with open("2022chcmp_teams.json") as file:
        teams = json.load(file)
        for team in teams:
            Team.objects.create(name=team['nickname'], number=team['team_number'], frc_key=team['key'])\


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