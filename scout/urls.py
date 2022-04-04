from django.urls import path
from . import views

# URLs 
app_name = 'scout'
urlpatterns = [
    path('', views.public_view, name='scout_home'),
    path('teams/', views.teams, name='teams'),
    path('matches/', views.matches, name='matches'),
    path('teams/<int:number>', views.team_summary, name='team_summary'),
    path('create_robot/', views.RobotCreateView.as_view(), name='create_robot'),
    path('submit_match/', views.MatchCreateView.as_view(), name='submit_match'),
]