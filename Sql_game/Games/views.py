from django.shortcuts import render,HttpResponse
import mysql.connector as msql
from django.db import connection
from django.contrib.auth import authenticate,login
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import *

from Games import models
def landing_page(request):
    if request.user.is_authenticated:
        return render(request,'Landingpage.html',{"is_logged":request.user.is_authenticated})
    else:
        return render(request,'Landingpage.html',{"is_logged":request.user.is_authenticated})
  

def Check_answer(Answer,seq_id):
    with connection.cursor() as cursor:
            cursor.execute(f"select Expected_answer from missing_truth where id={seq_id}")
            data=cursor.fetchone()
            result=data[0]
            print(result)
            if result.lower().strip()==Answer.lower().strip():
                return True
            else:
                return False
def Fetch_level(Next_level):
    with connection.cursor() as cursor:
        cursor.callproc(f"level_details",[Next_level])
        return cursor.fetchone()
def Exe_User_Query(Query):
    with connection.cursor() as cursor:
        if Query:
            cursor.execute(f"{Query}")
            resulted_data=cursor.fetchall()
            schema=cursor.description
            return resulted_data,schema
        else:
            return None,None


@login_required            
def Murder_mystery(request):
    username=request.session.get("username")
    try:
        user=User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("you have not logged in , Please go back and login ")
    try:
        Game_user=User_game_details.objects.get(userId_id=user.pk,gameId_id=1)
    except User_game_details.DoesNotExist:
        Game_user=User_game_details(userId_id=user.pk,gameId_id=1,curr_level=1,status="Not completed",score=0)
        Game_user.save() 

    with connection.cursor() as cursor:
        level_details=Fetch_level(Game_user.curr_level)
        promt,scene=level_details[4] ,level_details[3]  
        result=""
        if request.method=="POST" :
            
            
            if "run" in request.POST:
                Query=request.POST.get("user_query")
                print(Query)
                resulted_data,schema=Exe_User_Query(Query)
                print(resulted_data)
                # code for retriving heading of the resulted table
        
                return render(request,'murder_mystery.html',{"story":promt,"resulted_data":resulted_data,"schema":schema,"user":Game_user})
            
            if "ans-button" in request.POST:
                ans=request.POST.get("answer")
                print(Check_answer(ans,Game_user.curr_level))
                if Check_answer(ans,Game_user.curr_level):
                    print("You got the answer")
                    Level_details=Fetch_level(Game_user.curr_level)
                    points=level_details[6]
                    Game_user.score=Game_user.score+int(points)
                    seq_id=Game_user.curr_level+1
                    Game_user.curr_level=seq_id
                    Game_user.save()
                
                    Level_details=Fetch_level(Game_user.curr_level)
                    promt,scene=Level_details[4] ,Level_details[3]
                    render(request,'murder_mystery.html',{"story":promt,"scene-title":scene,"user":Game_user})   
                else:
                    print("Wrong answer")
         
        
            Query=request.POST.get("query")
            result=Exe_User_Query(Query)
    return render(request,'murder_mystery.html',{"story":promt,"scene-title":scene,"Query Result":result,"user":Game_user}) 
def user_login(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        Myuser=authenticate(request,username=username,password=password)
        if Myuser is not None:
            login(request,Myuser)
            request.session["username"]=Myuser.username
            return render(request,'Landingpage.html',{"is_authenticated":request.user.is_authenticated})
        else:
            return HttpResponse("Wrong username or password")
    else:
        return render(request,'login_page.html')
def user_signup(request):
    if request.method=="POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        password1=request.POST.get("pass1")
        password2=request.POST.get("pass2")
        if password1!=password2:
            return HttpResponse("Your password doesn't match ")
        else:
            My_user=User.objects.create_user(username,email,password1)
            return render(request,'After_signup.html')
    return render(request,'signup.html')


def leaderboard(request):
    leaderboard_objects=Leaderboard.objects.all().order_by('-score')
    context={"leaderboard":leaderboard_objects}
    return render(request,'leaderboard.html',context)
'''
def Locke_key(request):
    render(request,'locke_Key.html')'''
