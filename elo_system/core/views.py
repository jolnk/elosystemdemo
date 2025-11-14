# logica
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import PlayerForm, TeamForm, MatchForm, NewsForm
from .models import Player, Team, Match, News

def is_admin(user):
    return user.is_superuser

# REGISTRAR PLAYER (admin only)
@user_passes_test(is_admin)
def register_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()  # salva o jogador na database
            return redirect('home')  # redireciona pra página inicial depois de salvar
    else:
        form = PlayerForm()  # cria o formulário vazio para GET

    return render(request, 'core/register_player.html', {'form': form})  # passa o formulário para o template


# REGISTRAR TIMES (admin only)
@user_passes_test(is_admin)
def register_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            team = form.save()  # salva o time
            # agora associamos os jogadores selecionados ao time
            selected_players_ids = request.POST.getlist('players')  # pega os IDs dos jogadores selecionados
            selected_players = Player.objects.filter(id__in=selected_players_ids)
            team.players.set(selected_players)  # associa os jogadores ao time
            team.average_rating = sum(player.rating for player in team.players.all()) / len(team.players.all())
            team.save()
            return redirect('home')
    else:
        form = TeamForm()
        players = Player.objects.all()  # pega todos os jogadores para a seleção
    return render(request, 'core/register_team.html', {'form': form, 'players': players})  # passa a lista de jogadores pra template



# REGISTRAR PARTIDA (admin only)
@user_passes_test(is_admin)
def register_match(request):
    teams = Team.objects.all()  # pega todos os times registrados
    if request.method == 'POST':
        form = MatchForm(request.POST)
        if form.is_valid():
            match = form.save()

            # obtemos os times A e B a partir da partida
            team_a = match.team_a
            team_b = match.team_b

            # calcula o Elo entre os times (conforme a lógica anterior)
            new_rating_a, new_rating_b = match.calculate_elo(
                team_a.average_rating, team_b.average_rating, match.score_a
            )

            # atualiza os ratings dos times
            team_a.average_rating = new_rating_a
            team_b.average_rating = new_rating_b
            team_a.save()
            team_b.save()

            # depois disso, tem a atualizacao do rating de cada jogador de ambos os times com base no resultado da partida
            for player in team_a.players.all():
                # calcula o novo rating de cada jogador do time A
                expected_a = 1 / (1 + 10 ** ((team_b.average_rating - player.rating) / 400))
                new_player_rating_a = player.rating + 32 * (match.score_a - expected_a)
                player.rating = new_player_rating_a
                player.save()

            for player in team_b.players.all():
                # calcula o novo rating de cada jogador do time B
                expected_b = 1 / (1 + 10 ** ((team_a.average_rating - player.rating) / 400))
                new_player_rating_b = player.rating + 32 * (match.score_b - expected_b)
                player.rating = new_player_rating_b
                player.save()

            # redirect pra página inicial após registrar a partida
            return redirect('home')
    else:
        form = MatchForm()

    # passa o formulário de partida para o template
    return render(request, 'core/register_match.html', {'form': form, 'teams': teams})


# HOME VIEW (publica, lista histórico de partidas e ranking de jogadores)
def home(request):
    matches = Match.objects.all().order_by('-date')
    players = Player.objects.all().order_by('-rating')
    news = News.objects.all().order_by('-id')  # pegando notícias    #apagar para remover sistema de noticias

    return render(request, 'core/home.html', {
        'matches': matches,
        'players': players,
        'news': news,  # enviando notícias para o template    #apagar para remover sistema de noticias
    })




# SUBMENU
def manage(request):
    return render(request, 'core/manage.html')




###########################################################
# VISUALIZAR TODOS TIMES (apenas admin)
@user_passes_test(is_admin)
def view_teams(request):
    teams = Team.objects.all()  # Pega todos os times registrados
    return render(request, 'core/view_teams.html', {'teams': teams})



# VISUALIZAR TODOS JOGADORES (admin only)
@user_passes_test(is_admin)
def view_players(request):
    players = Player.objects.all().order_by('-rating')  # ordena pelo rating
    return render(request, 'core/view_players.html', {'players': players})




###########################################################
# X DELETAR TIME (admin only)
@user_passes_test(is_admin)
def delete_team(request, team_id):
    team = Team.objects.get(id=team_id)
    team.delete()
    return redirect('view_teams')

# X DELETAR JOGADOR (admin only)
@user_passes_test(is_admin)
def delete_player(request, player_id):
    player = Player.objects.get(id=player_id)
    player.delete()
    return redirect('view_players')




###########################################################
# VER TODAS AS PARTIDAS (apenas admin)
@user_passes_test(is_admin)
def view_matches(request):
    matches = Match.objects.all().order_by('-date')
    return render(request, 'core/view_matches.html', {'matches': matches})


# DELETAR PARTIDA (apenas admin)
@user_passes_test(is_admin)
def delete_match(request, match_id):
    match = Match.objects.get(id=match_id)
    match.delete()
    return redirect('view_matches')











@user_passes_test(is_admin)
def reset_all(request):
    if request.method == "POST":

        # deleta partidas (não tem fotos)
        for match in Match.objects.all():
            match.delete()

        # deleta times (chama delete individual -> apaga fotos)
        for team in Team.objects.all():
            team.delete()

        # deleta jogadores (chama delete individual -> apaga fotos)
        for player in Player.objects.all():
            player.delete()

        # deleta notícias (chama delete individual -> apaga imagem)
        for news in News.objects.all():
            news.delete()

        return redirect('home')

    return render(request, 'core/confirm_reset_all.html')













#######noticias
@user_passes_test(is_admin)
def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = NewsForm()

    return render(request, 'core/create_news.html', {'form': form})







# Visualizar todas as notícias (apenas admin)
@user_passes_test(is_admin)
def view_news(request):
    news_list = News.objects.all().order_by('-created_at')
    return render(request, 'core/view_news.html', {'news_list': news_list})


# Deletar notícia (apenas admin)
@user_passes_test(is_admin)
def delete_news(request, news_id):
    news = News.objects.get(id=news_id)
    news.delete()   # o sinal post_delete já remove a imagem
    return redirect('view_news')

