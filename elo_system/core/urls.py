# core/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views  # Importando as views de auth do Django
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # url inicial
    path('login/', auth_views.LoginView.as_view(), name='login'),  # url para login
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # url para logout
    path('register_player/', views.register_player, name='register_player'),
    path('register_team/', views.register_team, name='register_team'),
    path('register_match/', views.register_match, name='register_match'),  # url de registro de partida
    path('view_teams/', views.view_teams, name='view_teams'),  # mostrar todos times
    path('view_players/', views.view_players, name='view_players'), # mostrar todos jogadores
    path('delete_team/<int:team_id>/', views.delete_team, name='delete_team'), # apagar jogador
    path('delete_player/<int:player_id>/', views.delete_player, name='delete_player'), # apagar time
    path('view_matches/', views.view_matches, name='view_matches'), # mostrar todas as partidas
    path('delete_match/<int:match_id>/', views.delete_match, name='delete_match'), # apagar partidas
    path('reset_all/', views.reset_all, name='reset_all'), # wipe
    path('create_news/', views.create_news, name='create_news'), 
    path('view_news/', views.view_news, name='view_news'), # mostrar todas as noticias
    path('delete_news/<int:news_id>/', views.delete_news, name='delete_news'), # apagar noticias
    path('manage/', views.manage, name='manage'), # submenu para admins
]
