from django.shortcuts import render
from django.http import HttpResponse, request

import urllib3
import certifi
import json

from .models import Team

# Create your views here.
def public_view(request):
    # return HttpResponse("Public View")
    return render(request, 'scout/base.html')

def teams(request):
    return render(request, 'scout/teams.html')

def update_event(request):
    url = "https://www.thebluealliance.com/api/v3/event/2020chcmp/teams/simple"
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