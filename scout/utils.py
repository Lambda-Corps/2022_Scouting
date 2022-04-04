from .models import Team

import urllib3
import certifi
import json

def get_event_json(url):
    accept_header = 'application/json'
    auth_key = 'BJG4S2d2nkSkXikztbXHWBL8riwfb4ghAhUIXJ5dezxxhBpvC8ngqrekG2kjF5JV'
    headers = {
        'accept' : 'application/json',
        'X-TBA-Auth-Key' : auth_key,
        'User-Agent' : '1895_Scouter'
    }

    http = urllib3.PoolManager(ca_certs=certifi.where())
    req = http.request('GET', url, headers)

    return json.loads(req.data.decode('UTF-8'))


def update_event_teams():
    url = "https://www.thebluealliance.com/api/v3/event/2022chcmp/teams/simple"
    teams = get_event_json(url)

    # for team in teams:
    #     Team.objects.create(name=team['nickname'], number=team['team_number'], frc_key=team['key'])

    print(f"Found {len(teams)} in response")
    # Team.save()

    # return HttpResponse(teams)


def update_event_teams_json():
    teams = {}
    with open("2022chcmp_teams.json") as file:
        teams = json.load(file)
        for team in teams:
            Team.objects.create(name=team['nickname'], number=team['team_number'], frc_key=team['key'])


def get_frc_match_json():
    url = 'https://www.thebluealliance.com/api/v3/event/2022dc320/matches/simple'
    # url = 'https://www.thebluealliance.com/api/v3/event/2022chcmp/matches/simple'

    return get_event_json(url)


def get_qualifier_match(number):
    matches = get_frc_match_json()

    for match in matches:
        if match['comp_level'] == "qm" and match['match_number'] == number:
            return match

    # didn't get a match that hit
    return None


