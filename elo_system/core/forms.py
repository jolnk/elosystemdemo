# formularios
from django import forms
from .models import Player, Team, Match, News

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['username', 'rating', 'photo']  # inclui 'username', 'rating' e 'photo'


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'players', 'photo']
    
    # aqui da pra ajustar o widget do campo players pra um select com múltiplas opcoes
    players = forms.ModelMultipleChoiceField(
        queryset=Player.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # isso aq cria checkboxes pra selecionar múltiplos jogadores
    )
    

class MatchForm(forms.ModelForm):
    class Meta:
        model = Match
        fields = ['team_a', 'team_b', 'score_a', 'score_b']
    
    # definindo os campos de times como ModelChoiceField
    team_a = forms.ModelChoiceField(queryset=Team.objects.all(), label='Time A')
    team_b = forms.ModelChoiceField(queryset=Team.objects.all(), label='Time B')


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'image']
