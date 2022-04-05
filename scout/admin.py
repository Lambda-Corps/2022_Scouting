from django.contrib import admin

# Register your models here.
from .models import MatchResult, Team

admin.site.register(MatchResult)
admin.site.register(Team)