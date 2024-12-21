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

def profile(request):
    mydb,cursor=database()
    current_user=request.user
    username=current_user.username
    
    c="select Contest_Id,Accuracy from ml_participant where Status='Approved' and (Email1='{}' or Email2='{}' or Email3='{}')".format(username,username,username)
    cursor.execute(c)
    contestId = cursor.fetchall()
    
    data=dict()
    contests=[]
    for x in contestId:
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
        for x in result:
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
    except:
        1    
            
    
    return render(request,"User_Profile.html",data)

def editUserInfo(request):
    mydb,cursor=database()
    data = dict()
    current_user=request.user
    username=current_user.username
    if request.method=="POST":
        try:
            image = request.FILES['image']
            image_base64 = base64.b64encode(image.read()).decode('utf-8')
            c="update user_info set Profile_Pic = '{}' where Email = '{}'".format(image_base64,username)
            cursor.execute(c)
            mydb.commit()
        except:
            1
        try:
            name=request.POST['name']
            c="update user_info set Name = '{}' where Email = '{}'".format(name,username)
            cursor.execute(c)
            mydb.commit()
        except:
            1    
        try:
            university=request.POST['university']
            c="update user_info set University = '{}' where Email = '{}'".format(university,username)
            cursor.execute(c)
            mydb.commit()
        except:
            1               
            
    return redirect('profile') 

def ml_contest_home(request):
    if request.method=="GET":
        try:
            contestId=request.GET['contestId']
            current_user=request.user
            email=current_user.username
        
            mydb,cursor=database()
            data = dict()
            c = "select * from ml_contest where Id = '{}'".format(contestId)
            cursor.execute(c)
            result = cursor.fetchone()
            date_obj = datetime.strptime(str(result[3]), "%Y-%m-%d")
            cDate = date_obj.strftime("%Y-%m-%d") 
            
        
            time = str(result[4])
            data['year'] = cDate[:4]
            data['month'] = cDate[5:7]
            data['day'] =cDate[8:]
            #data['day'] = '22'
            
            data['hour']= time[:2]
            data['min']= time[2:5]
            data['sec']= time[5:]
            
            data['uid']=email
            data['cid']=contestId
            data['contestTitle']=result[1]
            data['aboutContest']=result[2]
            data['contestDate']=cDate
            data['contestTime']=result[4]
            data['aboutDataset']=result[5]
            data['submissionGuideLine']=result[6]
            data['datasetLink'] = "https://drive.google.com/drive/folders/1TWFzW71D1PfwTuMjJOXplhxdoHQFB2TC?usp=sharing"
        
            image_bytes = base64.b64decode(result[11])  
            image = Image.open(io.BytesIO(image_bytes))

            resized_image = image.resize((1200, 500))
            resized_image_bytes = io.BytesIO()
            resized_image.save(resized_image_bytes, format='PNG')
            data['image']= base64.b64encode(resized_image_bytes.getvalue()).decode('utf-8')
            data['pic']=userProfilePic(email)
        except:
            1    
        

        
        try:
            c="select Contest_Id from ml_participant where Contest_Id = '{}' and Status != '{}' and (Email1= '{}' or Email2='{}' or Email3='{}')".format(contestId,'Pending',email,email,email)
            cursor.execute(c)
            result=cursor.fetchone()
            if len(result[0])==0:
             data=dict()
        except:
             data=dict()  
             data['cid']='1'  
   
                 
    return render(request,"ml_contest_home_page.html",data)



def ml_submissions(request):
    data=dict()
    if request.method=="GET":
        contestId=request.GET['contestId']
        current_user=request.user
        email=current_user.username
        mydb,cursor=database()
        c="select Contest_Id from ml_participant where Contest_Id = '{}' and Status != '{}' and (Email1= '{}' or Email2='{}' or Email3='{}')".format(contestId,'Pending',email,email,email)
        cursor.execute(c)
        result=cursor.fetchone()
        try:
            flag = len(result[0])
        except:
            flag=0    
            data['cid'] = '1'
        if flag != 0:
            try:
                c="select * from {}".format(contestId)
                cursor.execute(c)
                result=cursor.fetchall()
                
                data['rows']=len(result)
                data['columns']=len(result[0])
            
                c = "select * from ml_contest where Id = '{}'".format(contestId)
                cursor.execute(c)
                result = cursor.fetchone()
                date_obj = datetime.strptime(str(result[3]), "%Y-%m-%d")
                cDate = date_obj.strftime("%Y-%m-%d") 
                
            
                time = str(result[4])
                data['year'] = cDate[:4]
                data['month'] = cDate[5:7]
                data['day'] =cDate[8:]
                #data['day'] = '22'
                
                data['hour']= time[:2]
                data['min']= time[2:5]
                data['sec']= time[5:]
                

                
                data['uid']=email
                data['cid']=contestId
                data['pic']=userProfilePic(email)
            except:
                data['cid']='1'  

    return render(request,"ml_submissions.html",data)

def file_Submit(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file'].read().decode('utf-8').splitlines()
        userId=request.POST['userId']
        contestId=request.POST['contestId']
        reader = csv.reader(csv_file)
        csv_data = [row for row in reader]
        
        mydb,cursor=database()
        c="select * from {}".format(contestId)
        cursor.execute(c)
        result=cursor.fetchall()
        counter = 1
        accuracy = 0
   
        number_of_rows = len(csv_data)
        for x in result[1:]:
            if x[0] == csv_data[counter][0] and x[1] == csv_data[counter][1]:
                accuracy = accuracy + 1
            counter=counter+1
                
            
        accuracy = (accuracy / (number_of_rows - 1) ) * 100
        
        c="select NumberOfEntry from ml_participant where Contest_Id='{}' and  Email1='{}' or Email2='{}' or Email3='{}'".format(contestId,userId,userId,userId)
        cursor.execute(c)
        result=cursor.fetchall()
        entry = int(result[0][0]) + 1
        
        
        current_datetime = datetime.now()
        time_str = str(current_datetime.strftime("%H:%M:%S"))

        
     
        c="update ml_participant set Accuracy='{}', LastSubmit='{}', NumberOfEntry='{}' where Contest_Id='{}' and Email1='{}' or Email2='{}' or Email3='{}'".format(accuracy,time_str,entry,contestId,userId,userId,userId)
        cursor.execute(c)
        mydb.commit()
        
        
    return redirect('ml_leaderboard', contest_id=contestId) 

def imageMaker(image):
    try:
        image_bytes = base64.b64decode(image)  
        image = Image.open(io.BytesIO(image_bytes))

        resized_image = image.resize((40,40))
        resized_image_bytes = io.BytesIO()
        resized_image.save(resized_image_bytes, format='PNG')
        image= base64.b64encode(resized_image_bytes.getvalue()).decode('utf-8')
        return image
    except:
        return ''    

def ml_leaderboard(request,contest_id):
    mydb,cursor = database()
    data=dict()
    c="select Team,Accuracy,Email1,Email2,EMail3,NumberOfEntry,LastSubmit from ml_participant where Contest_Id='{}' and Accuracy!='{}' order by Accuracy desc, LastSubmit asc".format(contest_id,0.0)
    cursor.execute(c)
    result = cursor.fetchall()
    teams=[]
    i=1
   
    for x in result:
        img1=img2=img3=''
        try:
            c="select Profile_Pic from user_info where Email = '{}'".format(x[2])
            cursor.execute(c)
            img = cursor.fetchone()
            img1 = imageMaker(img[0])
        except:
            1
                
        try:
            c="select Profile_Pic from user_info where Email = '{}'".format(x[3])
            cursor.execute(c)
            img = cursor.fetchone()
            img2 = imageMaker(img[0])
        
        except:
         1
        
        try:
            c="select Profile_Pic from user_info where Email = '{}'".format(x[4])
            cursor.execute(c)
            img = cursor.fetchone()
            img3 = imageMaker(img[0])
        except:
            1    
        
        team = {
            'serial': i,
            'team': x[0],
            'accuracy': x[1],
            'entry' : x[5],
            'last_submit' : x[6],
            'img1': img1,
            'img2': img2,
            'img3': img3
        }
        i=i+1
        teams.append(team)
    data['teams'] = teams
    data['cid']=contest_id
    current_user=request.user
    email=current_user.username
    data['pic']=userProfilePic(email)
    return render(request,"ml_leaderboard.html",data)
