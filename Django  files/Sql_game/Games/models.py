from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser,User

# Create your models here.
class Games_data(models.Model):
    game_name=models.CharField(max_length=64)
    difficulty=models.CharField(max_length=64)

    def __str__(self):
        return f"{self.game_name}"
    

class GamesStory(models.Model):
    level_no=models.IntegerField()
    sub_level_no=models.IntegerField()
    scene_name=models.TextField()
    prompt=models.TextField()
    Expected_answer=models.TextField()
    points=models.IntegerField()
    hint_text=models.TextField()
    hint_link=models.TextField()
    gameID=models.ForeignKey(Games_data,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.level_no}"
class User_game_details(models.Model):
    userId=models.ForeignKey(User,on_delete=models.CASCADE)
    gameId=models.ForeignKey(Games_data,on_delete=models.CASCADE)
    curr_level=models.IntegerField()
    score=models.IntegerField()
    status=models.CharField(max_length=64)
class Leaderboard(models.Model):
    userID=models.ForeignKey(User,on_delete=models.CASCADE)
    score=models.IntegerField()




       

