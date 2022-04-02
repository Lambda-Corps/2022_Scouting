from django.urls import path
from . import views

# URLs 
urlpatterns = [
    path('', views.public_view, name='scout_home'),
    path('teams/', views.teams, name='teams'),
    path('matches/', views.public_view, name='matches')
]