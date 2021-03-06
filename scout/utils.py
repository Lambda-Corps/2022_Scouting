from .models import Team, MatchResult, Robot

import urllib3
import certifi
import json
import random

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

    for team in teams:
        Team.objects.create(name=team['nickname'], number=team['team_number'], frc_key=team['key'])

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
    # url = 'https://www.thebluealliance.com/api/v3/event/2022dc320/matches/simple'
    url = 'https://www.thebluealliance.com/api/v3/event/2022chcmp/matches/simple'

    return get_event_json(url)


def get_qualifier_match(number):
    matches = get_frc_match_json()

    for match in matches:
        if match['comp_level'] == "qm" and match['match_number'] == number:
            return match

    # didn't get a match that hit
    return None


def get_playoff_match(type, number):
    matches = get_frc_match_json()

    for match in matches:
        if match['comp_level'] == type and match['match_number'] == number:
            return match

    # didn't find one
    return None


def get_frckey_scoring_dict(frckey):
    team = Team.objects.get(frc_key=frckey)

    if team is None:
         return None

    auto_points, teleop_points, endgame_points = get_team_scoring_prediction(team.number)

    return {'number': team.number, 'auto_points': auto_points, 'teleop_points': teleop_points, 'endgame_points': endgame_points} 


def get_team_scoring_prediction(number):
    matches = {}
    team = {}
    try:
        team = Team.objects.get(frc_key=number)
        matches = team.matches.all()
    except Team.DoesNotExist:
        return {'number': 1, 'auto_points': 1, 'teleop_points': 2, 'endgame_points': 3}
    
    # print(matches)
    match_count = matches.count()

    if match_count == 0:
        # use prediction from pit scout
        return {'number': team.number, 'auto_points': 1, 'teleop_points': 2, 'endgame_points': 3}
    else:
        # Sum up the matches and give an average
        auto_taxi = 0.0
        auto_cargo = 0.0
        teleop_cargo = 0.0
        endgame_total = 0.0
        climbs_attempted = 0.0

        for match in matches:
            if match.auto_taxi is True:
                auto_taxi += 2

            if match.auto_scored > 0:
                #auto_cargo += match.auto_scored * 2 if match.auto_target is 'Low Goal' else 4
                auto_cargo += match.auto_scored

            if match.tele_low > 0:
                teleop_cargo += match.tele_low

            if match.tele_high > 0:
                #teleop_cargo += match.tele_high * 2
                teleop_cargo += match.tele_high 

            if match.climb_attempted:
                climbs_attempted += 1
                endgame_total += match.climb_points
        
        # Return the total expected points based on results
        auto_points = round((auto_taxi/match_count) + (auto_cargo/match_count), 2)
        teleop_points = round(teleop_cargo / match_count, 2)
        endgame_points = round(endgame_total / match_count, 2)

        return {'number': team.number, 'auto_points': auto_points, 'teleop_points': teleop_points, 'endgame_points': endgame_points}


def team_match_generator(matches_per_team):
    # Possible field entries
    auto_target_field = ['High Goal', 'Low Goal']
    tele_target_field = ['High Goal', 'Low Goal']
    climb_height_field = [0, 4, 6, 10, 15]
    driver_rating_field = [1, 2, 3, 4, 5]

    teams = Team.objects.all()

    for team in teams:
        for x in range(1, matches_per_team):
            result = MatchResult(frc_team=team,
                                match_number=x,
                                auto_taxi=random.randint(0,1) == 0,
                                auto_scored=random.randint(0,5),
                                auto_target=auto_target_field[random.randint(0,1)],
                                tele_low=random.randint(0,3),
                                tele_high=random.randint(0,6),
                                climb_points=climb_height_field[random.randint(0,4)],
                                climb_attempted=random.randint(0,1)==0,
                                driver_rating=driver_rating_field[random.randint(0,4)],
                                comments="Auto-generated Match"
                                )
            result.save()

def event_match_generator(number_of_matches):
    # frc_team = models.ForeignKey(Team, related_name='matches', null=True , on_delete=models.CASCADE)
    # match_number = models.IntegerField(default=0)
    # auto_taxi = models.BooleanField(default=False)
    # auto_scored = models.IntegerField(default=0)
    # auto_target = models.CharField(choices=auto_target_field, default=NONE, max_length=13)
    # tele_low = models.PositiveSmallIntegerField(default=0)
    # tele_high = models.IntegerField(default=0)
    # climb_points = models.PositiveSmallIntegerField(choices=climb_height_field, default=0)
    # climb_attempted = models.BooleanField(default=False)
    # driver_rating = models.CharField(choices=driver_rating_field, default=ONE, max_length=13)
    # comments = models.CharField(max_length=250, default='No comments')

    # Possible field entries
    auto_target_field = ['High Goal', 'Low Goal']
    tele_target_field = ['High Goal', 'Low Goal']
    climb_height_field = [0, 4, 6, 10, 15]
    driver_rating_field = [1, 2, 3, 4, 5]
    
    for x in range(number_of_matches):
        result = MatchResult(frc_team=get_random_team(),
                             match_number=random.randint(1,number_of_matches),
                             auto_taxi=random.randint(0,1) == 0,
                             auto_scored=random.randint(0,5),
                             auto_target=auto_target_field[random.randint(0,1)],
                             tele_low=random.randint(0,3),
                             tele_high=random.randint(0,6),
                             climb_points=climb_height_field[random.randint(0,4)],
                             climb_attempted=random.randint(0,1)==0,
                             driver_rating=driver_rating_field[random.randint(0,4)],
                             comments="Auto-generated Match"
                            )
        result.save()



def get_random_team():
    teams = Team.objects.all()

    team_numbers = []
    for team in teams:
        team_numbers.append(team.number)

    return Team.objects.get(number=team_numbers[random.randint(0, len(team_numbers))])


def pit_scout_generator():
    tele_goal = ['Low', 'High', 'Both', 'None']
    climb_level = ['Low Bar', 'Middle Bar', 'High Bar', 'Traversal Bar', 'No Climb']
    drive_type_choices = ['WCD', 'Swerve', 'Mechanum', 'KoP Chassis']
    # frc_team = models.OneToOneField(Team, related_name='robot', null=True, on_delete=models.CASCADE,verbose_name="Team")
    # auto_points = models.IntegerField(default=0)
    # drive_type = models.CharField(max_length=45)
    # target = models.CharField(choices=tele_goal, max_length=11)
    # climb = models.CharField(choices=climb_level, max_length=13)

    teams = Team.objects.all()

    for team in teams:
        robot = Robot(
            frc_team=team,
            auto_points=random.randint(0,22),
            drive_type=drive_type_choices[random.randint(0,3)],
            target=tele_goal[random.randint(0,3)],
            climb=climb_level[random.randint(0,4)]
        )

        robot.save()
