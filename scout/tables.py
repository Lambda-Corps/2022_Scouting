import django_tables2 as tables
from .models import Team #TeamEfficiency, Match, Robot
from django_tables2.utils import A

class TeamTable(tables.Table):
    number = tables.LinkColumn('scout:team_summary', args=[A('number')])

    class Meta:
        model = Team
        template_name = 'django_tables2/bootstrap.html'
        fields = ['number', 'name']