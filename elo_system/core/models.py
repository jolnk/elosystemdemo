# modelos
from django.db import models
from django.contrib.auth.models import User

# MODEL PARA JOGADOR

class Player(models.Model):
    username = models.CharField(max_length=100, unique=True)  # adiciona unique=True para garantir que o username seja único
    rating = models.IntegerField(default=1500)  # valor padrao de 1500
    photo = models.ImageField(upload_to='player_photos/', null=True, blank=True)

    def __str__(self):
        return self.username

# MODEL PARA TIME
class Team(models.Model):
    name = models.CharField(max_length=100)
    players = models.ManyToManyField(Player)
    photo = models.ImageField(upload_to='team_photos/', blank=True, null=True)
    average_rating = models.FloatField(default=1200)

    def __str__(self):
        return self.name

# MODEL PARA PARTIDA
class Match(models.Model):
    team_a = models.ForeignKey(Team, related_name='team_a_matches', on_delete=models.CASCADE)
    team_b = models.ForeignKey(Team, related_name='team_b_matches', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    score_a = models.FloatField()
    score_b = models.FloatField()

    def __str__(self):
        return f"{self.team_a.name} vs {self.team_b.name} - {self.date}"

    def calculate_elo(self, rating_a, rating_b, score_a, k=32):
        expected_a = 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
        score_b = 1 - score_a
        new_rating_a = rating_a + k * (score_a - expected_a)
        new_rating_b = rating_b + k * (score_b - (1 - expected_a))
        return new_rating_a, new_rating_b



# MODEL PARA PARTIDA
class News(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='news_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


###########################################################################



#   related a deletar a foto se o time ou jogador for apagado.
#   nao é preciso nenhum codigo adicional em outros arquivos, somente neste.             <-  !
#   apagar ou comentar as linhas de baixo faz com que as fotos permaneçam salvas


from django.db.models.signals import post_delete
from django.dispatch import receiver
import os

@receiver(post_delete, sender=Player)
def delete_player_photo(sender, instance, **kwargs):
    if instance.photo and instance.photo.path and os.path.isfile(instance.photo.path):
        os.remove(instance.photo.path)


@receiver(post_delete, sender=Team)
def delete_team_photo(sender, instance, **kwargs):
    if instance.photo and instance.photo.path and os.path.isfile(instance.photo.path):
        os.remove(instance.photo.path)       


@receiver(post_delete, sender=News)
def delete_news_image(sender, instance, **kwargs):
    if instance.image and instance.image.path and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)
