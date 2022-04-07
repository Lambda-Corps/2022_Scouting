import django_tables2 as tables
from .models import MatchResult, Team #TeamEfficiency, Match, Robot
from django_tables2.utils import A

class TeamTable(tables.Table):
    number = tables.LinkColumn('scout:team_summary', args=[A('number')])
    robot = tables.Column(verbose_name="Robot")

    class Meta:
        model = Team
        template_name = 'django_tables2/bootstrap.html'
        fields = ['number', 'name', 'robot']


class MatchResultTable(tables.Table):
    frc_team = tables.LinkColumn('scout:team_summary', args=[A('frc_team.number')], verbose_name="Team")
    match_number = tables.LinkColumn('scout:edit_match', args=[A('match_number')])

    class Meta:
        model = MatchResult
        template_name = 'django_tables2/bootstrap.html'
        exclude = ['id']
