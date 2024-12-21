from django.shortcuts import render,redirect
import mysql.connector as sql
import pandas as pd
import numpy as np
import csv
from django.db import connection
from datetime import datetime
from PIL import Image
import base64
import io
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.contrib import messages

def database():
    mydb = sql.connect(
    host="localhost",
    user="root",
    password="",
    database="online_judge"
    )
    cursor=mydb.cursor()
    return mydb,cursor


def admin_dashboard(request):
    mydb,cursor=database()
    data = dict()
    c="select count(Name) from user_info"
    cursor.execute(c)
    result = cursor.fetchone()
    data['total_user']=result[0]
    
    c="select count(Id) from ml_contest"
    cursor.execute(c)
    result = cursor.fetchone()
    data['ml_contest'] = result[0]
    
    c="select count(Id) from ml_contest where Contest_Status = '{}'".format('Pending')
    cursor.execute(c)
    result = cursor.fetchone()
    data['ml_pending'] = result[0]
    
    c="select count(Id) from programming_contest"
    cursor.execute(c)
    result = cursor.fetchone()
    data['prog_contest'] = result[0]
    
    c="select count(Id) from programming_contest where Contest_Status = '{}'".format('Pending')
    cursor.execute(c)
    result = cursor.fetchone()
    data['prog_pending'] = result[0]
    
    data['total_contest']=int(data['prog_contest'])+int(data['ml_contest'])
    data['total_pending']=int(data['prog_pending'])+int(data['ml_pending'])
    
    c="select count(Contest_Id) from ml_participant"
    cursor.execute(c)
    result = cursor.fetchone()
    data['ml_team'] = result[0]
    
    c="select count(Contest_Id) from ml_participant where Email1!='{}'".format('')
    cursor.execute(c)
    member1 = cursor.fetchone()
    
    c="select count(Contest_Id) from ml_participant where Email2!='{}'".format('')
    cursor.execute(c)
    member2 = cursor.fetchone()
    
    c="select count(Contest_Id) from ml_participant where Email3!='{}'".format('')
    cursor.execute(c)
    member3 = cursor.fetchone()
    
    data['ml_member'] = int(member1[0])+int(member2[0])+int(member3[0])
    
    c="select count(Contest_Id) from programming_participant"
    cursor.execute(c)
    result = cursor.fetchone()
    data['prog_team'] = result[0]
    
    c="select count(Contest_Id) from programming_participant where Email1!='{}'".format('')
    cursor.execute(c)
    member1 = cursor.fetchone()
    
    c="select count(Contest_Id) from programming_participant where Email2!='{}'".format('')
    cursor.execute(c)
    member2 = cursor.fetchone()
    
    c="select count(Contest_Id) from programming_participant where Email3!='{}'".format('')
    cursor.execute(c)
    member3 = cursor.fetchone()
    
    data['prog_member'] = int(member1[0])+int(member2[0])+int(member3[0])
    
    c="select count(Email) from user_info where Role='{}'".format("Organizer")
    cursor.execute(c)
    result = cursor.fetchone()
    data['total_org']=result[0]
    

    return render(request,"admin_dashboard.html",data)

def ml_contest_list(username):
    mydb,cursor = database()
    contest_list = []
    if len(username) != 0:
        c = " select * from ml_contest order by Contest_Date"
        cursor.execute(c)
        result=cursor.fetchall()
    
        counter=1
        for x in result:
            contest = {
                'serial' : counter,
                'id' : x[0],
                'title' : x[1],
                'cdate' : x[3],
                'ctime' : x[4],
                'fee' : x[7],
                'rdate' : x[8],
                'authorId' : x[9],
                'status' : x[10]
            }
            counter = counter + 1
            contest_list.append(contest)
    return contest_list

def admin_ml_contest(request):
    current_user=request.user
    username=current_user.username
    data = dict()
    data['contest_list']=ml_contest_list(username)
    return render(request,"admin_ml_contest_list.html",data)

def admin_ml_contest_confirmation(request):
    if request.method=="POST":
        contestId = request.POST['contestId']
        mydb,cursor = database()
        c = "update ml_contest set Contest_Status = '{}' where Id='{}'".format('Approved',contestId)
        cursor.execute(c)
        mydb.commit()
         
    current_user=request.user
    username=current_user.username
    data = dict()
    data['contest_list']=ml_contest_list(username)
    return render(request,"admin_ml_contest_list.html",data)

def admin_ml_contest_remove_confirmation(request):
    if request.method=="POST":
        contestId = request.POST['contestId']
        mydb,cursor = database()
        c = "update ml_contest set Contest_Status = '{}' where Id='{}'".format('Pending',contestId)
        cursor.execute(c)
        mydb.commit()
         
    current_user=request.user
    username=current_user.username
    data = dict()
    data['contest_list']=ml_contest_list(username)
    return render(request,"admin_ml_contest_list.html",data)

def admin_ml_contest_details(request):
    if request.method == 'POST':
        mydb,cursor = database()
        contestId = request.POST['contestId']
        c = "select * from ml_contest where Id = '{}' order by Contest_Date".format(contestId)
        cursor.execute(c)
        result = cursor.fetchone()
        date_obj = datetime.strptime(str(result[3]), "%Y-%m-%d")
        cDate = date_obj.strftime("%Y-%m-%d") 
        date_obj = datetime.strptime(str(result[8]), "%Y-%m-%d")
        rDate = date_obj.strftime("%Y-%m-%d") 
        data = dict()
        data['cid']=contestId
        data['contestTitle']=result[1]
        data['aboutContest']=result[2]
        data['contestDate']=cDate
        data['contestTime']=result[4]
        data['aboutDataset']=result[5]
        data['submissionGuideLine']=result[6]
        data['contestFee']=result[7]
        data['registrationDate']=rDate
       
        try:
            image_bytes = base64.b64decode(result[11])  
            image = Image.open(io.BytesIO(image_bytes))
                
                # Resize the image to 300x300
            resized_image = image.resize((1200, 500))
            resized_image_bytes = io.BytesIO()
            resized_image.save(resized_image_bytes, format='PNG')
            data['image']= base64.b64encode(resized_image_bytes.getvalue()).decode('utf-8')
        except:
            1   
    return render(request,"admin_ml_contest_details.html",data) 

def userManagement(request):
    mydb,cursor=database()
    c="select * from user_info order by Role"
    cursor.execute(c)
    result = cursor.fetchall()
    data=dict()
    users=[]
    count = 0
    for x in result:
        count = count + 1
        user={
            'serial': count,
            'name': x[0],
            'id': x[1],
            'role': x[5],
            'university': x[3]
        }
        try:
            image_bytes = base64.b64decode(x[2])  
            image = Image.open(io.BytesIO(image_bytes))
                        
            resized_image = image.resize((60,60))
            resized_image_bytes = io.BytesIO()
            resized_image.save(resized_image_bytes, format='PNG')
            image = base64.b64encode(resized_image_bytes.getvalue()).decode('utf-8')
            user['image']=image
        except:
            user['image']=''   
        users.append(user)
    data['users']=users    
        
    return render(request,"user_management.html",data)

def give_org_acces(request):
    mydb,cursor = database()
    if request.method=="POST":
        userId = request.POST['userId']
        c="update user_info set Role = '{}' where Email = '{}'".format('Organizer',userId)
        cursor.execute(c)
        mydb.commit()
    
    return redirect('userManagement')

def remove_org_access(request):
    mydb,cursor = database()
    if request.method=="POST":
        userId = request.POST['userId']
        c="update user_info set Role = '{}' where Email = '{}'".format('Participant',userId)
        cursor.execute(c)
        mydb.commit()
    return redirect('userManagement')

def organizational_profile(request):
        
  data = dict()
  if request.method=="GET":
    username = request.GET['userId']

    mydb,cursor=database()
    c="select count(Id) from ml_contest where Author_Id = '{}'".format(username)
    cursor.execute(c)
    result=cursor.fetchone() 
    data['total'] = result[0]
    
    c="select count(Id) from ml_contest where Author_Id = '{}' and (Contest_Status = 'Pending' or  Contest_Status = 'Approved')".format(username)
    cursor.execute(c)
    result=cursor.fetchone()
    data['pending'] = result[0]
    
    c="select count(Id) from ml_contest where Author_Id = '{}' and Contest_Status = 'Completed'".format(username)
    cursor.execute(c)
    result=cursor.fetchone()
    data['complete'] = result[0]
    
    c="select Id from ml_contest where Author_Id = '{}'".format(username)
    cursor.execute(c)
    result=cursor.fetchall()
    
    numberOfTeam = 0
    participants = []
    for x in result:
       c="select count(Contest_Id) from ml_participant where Contest_Id = '{}'".format(x[0])
       cursor.execute(c)
       team = cursor.fetchone()
       numberOfTeam = numberOfTeam + int(team[0])
       c="select Title from ml_contest where Id = '{}'".format(x[0])
       cursor.execute(c)
       title = cursor.fetchone()
       participant={
           'title' : title[0],
           'number': team[0]
       }
       participants.append(participant)
       
       
    data['team'] = numberOfTeam
    participants.sort(key=lambda p: p['number'], reverse=True)

    data['participants'] = participants
    c="select Name from user_info where Email='{}'".format(username)
    cursor.execute(c)
    result=cursor.fetchone()
    data['name']=result[0]
    data['userId']=username
    
  
    return render(request,"organizational_profile.html",data)
def userProfilePic(username):
    mydb,cursor=database()

    c="select * from user_info where Email='{}'".format(username)
    cursor.execute(c)
    result=cursor.fetchone()
    image=''
    try:
        image_bytes = base64.b64decode(result[2])  
        image = Image.open(io.BytesIO(image_bytes))
                    
        resized_image = image.resize((300,300))
        resized_image_bytes = io.BytesIO()
        resized_image.save(resized_image_bytes, format='PNG')
        image = base64.b64encode(resized_image_bytes.getvalue()).decode('utf-8')
    except:
        1  
    return image  
def admin_user_profile(request):
    if request.method=='GET':
        username = request.GET['userId']
        mydb,cursor=database()

        c="select Contest_Id,Accuracy from ml_participant where Status='Approved' and (Email1='{}' or Email2='{}' or Email3='{}')".format(username,username,username)
        cursor.execute(c)
        contestId = cursor.fetchall()
        
        data=dict()
        contests=[]
        count=0
        for x in contestId:
            count=count+1
            c="select Title,Contest_Date from ml_contest where Id='{}'".format(x[0])
            cursor.execute(c)
            contest = cursor.fetchone()
            contestData = {
                'id': x[0],
                'title': contest[0],
                'date': contest[1],
                'accuracy': x[1]
            }
            contests.append(contestData)
        
        data['contests']=contests  
        data['ml_contest']=count
        c="select * from user_info where Email='{}'".format(username)
        cursor.execute(c)
        result=cursor.fetchone()
        data['userId']=username  
        try:
            data['username']=result[0]
        
            data['university']=result[3]
        except:
            1 
        data['pic']=userProfilePic(username)
        try:
            image_bytes = base64.b64decode(result[2])  
            image = Image.open(io.BytesIO(image_bytes))
                        
            resized_image = image.resize((300,300))
            resized_image_bytes = io.BytesIO()
            resized_image.save(resized_image_bytes, format='PNG')
            data['image']= base64.b64encode(resized_image_bytes.getvalue()).decode('utf-8')
        except:
            1    
        
        c="select Contest_Id from programming_participant where Status='Approved' and (Email1='{}' or Email2='{}' or Email3='{}')".format(username,username,username)   
        cursor.execute(c)
        result=cursor.fetchall() 

        try:
            contests = []
            count = 0
            for x in result:
                count=count+1
                c="select Title,Contest_Date from programming_contest where Id='{}'".format(x[0])
                cursor.execute(c)
                contest = cursor.fetchone()
                contestData = {
                    'id': x[0],
                    'title': contest[0],
                    'date': contest[1],
                
                }
                contests.append(contestData)
            data['programming']=contests  
            data['prog_contest'] = count
        except:
            1    
    return render(request,"admin_user_profile.html",data)

def programming_contest_list(username):
    
    if len(username) != 0:
        mydb,cursor = database()
        c = "select * from programming_contest order by Contest_Date"
        cursor.execute(c)
        result=cursor.fetchall()
        contest_list = []
        counter=1
        for x in result:
            contest = {
                'serial' : counter,
                'id' : x[0],
                'title' : x[1],
                'cdate' : x[4],
                'ctime' : x[5],
                'fee' : x[6],
                'rdate' : x[7],
                'author' : x[8],
                'status' : x[9]
            }
            counter = counter + 1
            contest_list.append(contest)
        return contest_list    
    


def admin_programming_contest_list(request):
    current_user=request.user
    username=current_user.username
    data = dict()
    data['contest_list']=programming_contest_list(username) 
    return render(request,"admin_programming_contest_list.html",data)

def admin_programming_contest_confirmation(request):
    if request.method=="POST":
        contestId = request.POST['contestId']
        mydb,cursor = database()
        c = "update programming_contest set Contest_Status = '{}' where Id='{}'".format('Approved',contestId)
        cursor.execute(c)
        mydb.commit()
            
    current_user=request.user
    username=current_user.username
    data = dict()
    data['contest_list']=programming_contest_list(username) 
    return render(request,"admin_programming_contest_list.html",data)

def admin_programming_contest_remove_confirmation(request):
    if request.method=="POST":
        contestId = request.POST['contestId']
        mydb,cursor = database()
        c = "update programming_contest set Contest_Status = '{}' where Id='{}'".format('Pending',contestId)
        cursor.execute(c)
        mydb.commit()    
    current_user=request.user
    username=current_user.username
    data = dict()
    data['contest_list']=programming_contest_list(username) 
    return render(request,"admin_programming_contest_list.html",data)

def admin_programming_contest_details(request):
    if request.method == 'POST':
        mydb,cursor = database()
        current_user=request.user
        username=current_user.username
        contestId = request.POST['contestId']
        c = "select * from programming_contest where Id = '{}' order by Contest_Date".format(contestId)
        cursor.execute(c)
        result = cursor.fetchone()
        date_obj = datetime.strptime(str(result[4]), "%Y-%m-%d")
        cDate = date_obj.strftime("%Y-%m-%d") 
        date_obj = datetime.strptime(str(result[7]), "%Y-%m-%d")
        rDate = date_obj.strftime("%Y-%m-%d") 
        data = dict()
        data['cid']=contestId
        data['contestTitle']=result[1]
        data['aboutContest']=result[2]
        data['rules']=result[3]
        data['contestDate']=cDate
        data['contestTime']=result[5]
        data['contestFee']=result[6]
        data['registrationDate']=rDate
        
        c="select * from user_info where Email='{}'".format(username)
        cursor.execute(c)
        user = cursor.fetchone()
        data['name']=user[0]
        data['email']=username
        data['University']=user[3]
        data['role']=user[5]
        try:
            image_bytes = base64.b64decode(user[2])  
            image = Image.open(io.BytesIO(image_bytes))
                
            resized_image = image.resize((160,160))
            resized_image_bytes = io.BytesIO()
            resized_image.save(resized_image_bytes, format='PNG')
            data['profilePic']= base64.b64encode(resized_image_bytes.getvalue()).decode('utf-8')
        except:
            1   
        
        try:
            image_bytes = base64.b64decode(result[10])  
            image = Image.open(io.BytesIO(image_bytes))

            resized_image = image.resize((1200, 500))
            resized_image_bytes = io.BytesIO()
            resized_image.save(resized_image_bytes, format='PNG')
            data['image']= base64.b64encode(resized_image_bytes.getvalue()).decode('utf-8')
        except:
            1   
    return render(request,"admin_programming_contest_details.html",data) 
            
    

