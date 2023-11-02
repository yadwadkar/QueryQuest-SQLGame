from django.contrib import admin
from django.urls import path,include
from Games import views
from django.contrib.auth.decorators import login_required
app_name="Games"
urlpatterns=[path("",views.landing_page,name="landing page"),
             path("game",login_required(views.Murder_mystery),name="game"),
             path("login",views.user_login,name="login"),
             path("signup",views.user_signup,name="signup"),
             path("leaderboard",views.leaderboard,name="leaderboard")]