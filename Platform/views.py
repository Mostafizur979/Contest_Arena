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
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail,EmailMultiAlternatives
import random

def database():
    mydb = sql.connect(
    host="localhost",
    user="root",
    password="",
    database="online_judge"
    )
    cursor=mydb.cursor()
    return mydb,cursor
def authentication(request):

    return render(request,"authentication.html")

#send otp
def register(request):
    data=dict()
    try:
        if request.method=='POST':
            name=request.POST['name']
            email=request.POST['user_mail']
            password = request.POST['password']
            subject="OTP Code"
            form_email="mlcodeverse@gmail.com"
            to=email
            msg='Your OTP Code is '
            otp=''
            for i in range(0,6):  
                otp=otp+str(random.randint(0, 9))
            msg=msg+otp    
            msg=EmailMultiAlternatives(subject,msg,form_email,[to])
            msg.content_subtype='html'
            msg.send()
            
            data['name']=name
            data['email']=email
            data['pass']=password
            data['otp']=otp

    except:
        data['msg'] = "This Email Id isn't exist"
        return render(request, 'authentication.html',data)
                
    return render(request, 'otp_verification.html',data)

def verification(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        passw=request.POST['password']
     
        user = User.objects.create_user(
            username = email,  
            password=passw 
        )
        data = dict()
        try:
            user.save()
            mydb,cursor=database()
            c="insert into user_info values('{}','{}','{}','{}','{}','{}')".format(name,email,'','','','')
            cursor.execute(c)
            mydb.commit()
            user = authenticate(username=email, password=passw)
            if user is not None:
                login(request, user)
                
                return redirect('profile')
            else:
                return redirect('authentication')
        except:
        
            data['error'] = "Already exist this acconunt."  
            return render(request, "otp_verification.html",data)  
        
    return redirect('oraganizational_dashboard')  

def signin(request):
    try:
        if request.method == 'POST':
            username = request.POST['uid']
            pass1 = request.POST['password']
            mydb,cursor = database()
            user = authenticate(username=username, password=pass1)
            if user is not None:
                login(request, user)
        
                c="select Role from user_info where Email='{}'".format(username)
                cursor.execute(c)
                accType = cursor.fetchone()
                role = accType[0]
                    
                if role=="Organizer":
                   return redirect('oraganizational_dashboard')  
                else:
                   return redirect('profile')         
            else:
                return redirect('authentication')
    except:
        1
    return render(request, "authentication.html")  

def logout_view(request):
    logout(request)  
    return redirect('Landing_Page')

def imageMaker(image):
    try:
        image_bytes = base64.b64decode(image)  
        image = Image.open(io.BytesIO(image_bytes))

        resized_image = image.resize((200,200))
        resized_image_bytes = io.BytesIO()
        resized_image.save(resized_image_bytes, format='PNG')
        image= base64.b64encode(resized_image_bytes.getvalue()).decode('utf-8')
        return image
    except:
        return ''   
    
def Landing_Page(request):
    data = dict()
    current_user=request.user
    username=current_user.username
    data['number_of_contests'] = '100'
    data['number_of_contestants'] = '10800'
    data['number_of_submissions'] = '200000'
    data['number_of_accepted'] = '100000'
    
    contest = dict()
    contests = []
    mydb,cursor=database()
    c="select Id,Title,Contest_Date,Contest_Time from ml_contest limit 2"
    cursor.execute(c)
    result = cursor.fetchall()
    for x in result:
        contest ={
            'id' : x[0],
            'title' : x[1],
            'date' : x[2],
            'time' : x[3] 
        }
        contests.append(contest)
    
    data['contests'] = contests
    try:
        c="select Profile_Pic,Role from user_info where Email = '{}'".format(username)
        cursor.execute(c)
        img = cursor.fetchone()
        data['role']=img[1]
        data['profilePic'] = imageMaker(img[0])
    except:
        data['profilePic'] = ''
    data['sessionId'] = username
    
    
    return render(request,"Landing_Page.html",data)


def Host_ML_Contest(request):
      current_user=request.user
      username=current_user.username
      data = dict()

      if len(username)==0 and 1==2:
        data={
            'login_status' : '0'
        }
        return render(request,"authentication.html",data) 
      else:
        data={
          'login_status' : '1'
        }

        mydb,cursor = database()
      
        csv_data = []
        contest_id = 0
        contest_id=0
        contest_title=0
        contest_description=0
        contest_date=0
        contest_time=0
        about_dataset=0
        submission_guideline=0
        contest_fee=0
        registration_date=0
        if request.method == 'POST' and request.FILES['csv_file']:
            try:
                print("Reach")
                csv_file = request.FILES['csv_file'].read().decode('utf-8').splitlines()
                contest_title = request.POST['contest_title']
                contest_description = request.POST['contest_description']
                contest_date_time = request.POST['contest_date_time']
                about_dataset = request.POST['about_dataset']
                submission_guideline = request.POST['submission_guideline']
                contest_fee = request.POST['contest_fee']
                registration_date = request.POST['registration_date']
                image_base64=''
                try:
                    image = request.FILES['banner']
                    image_base64 = base64.b64encode(image.read()).decode('utf-8')

                except:
                    print("'image' key not found in request.FILES")                
                        
                contest_date=contest_date_time[:10]
                contest_time=contest_date_time[11:]
                reader = csv.reader(csv_file)
                csv_data = [row for row in reader]
                current_date = datetime.now()
                current_month = current_date.month
                current_year = current_date.year
                current_day =current_date.day
                    
                date=str(current_year)+'-'+str(current_month)+'-'+str(current_day)
                date = str(date).replace('-', '')
                    
                c="select count(file_id) from csv_file_id"
                cursor.execute(c)
                result = cursor.fetchone()
                number_of_file = result[0] + 1
                contest_id='contest_id'+date[2:]+str(number_of_file)
                c = f"create table {contest_id} (col1 varchar(200), col2 varchar(200))"
                cursor.execute(c)
                mydb.commit()
                
                c = "insert into csv_file_id  values('{}')".format(contest_id)
                cursor.execute(c)
                mydb.commit()

                for x in csv_data:
                    c = "INSERT INTO {} (col1, col2) VALUES ('{}', '{}')".format(contest_id, x[0], x[1])
                    cursor.execute(c)
                    mydb.commit()
                            
                c="insert into ml_contest values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(contest_id,contest_title,contest_description,contest_date,contest_time,about_dataset,submission_guideline,contest_fee,registration_date,username,"Pending",image_base64)  
                cursor.execute(c)
                mydb.commit()
                host_contest_list(request)
            except:
                1    
            return redirect('host_contest_list')    
      return render(request, 'Host_Contest.html',data)
  
  
def host_contest_list(request):
    current_user=request.user
    username=current_user.username
    data = dict()
    mydb,cursor = database()
  
    if len(username) != 0:
        c = " select * from ml_contest where Author_Id = '{}' order by Contest_Date".format(username)
        cursor.execute(c)
        result=cursor.fetchall()
        contest_list = []
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
                'status' : x[10]
            }
            counter = counter + 1
            contest_list.append(contest)
        data['contest_list']=contest_list   
    return render(request,"host_contest_list.html", data)



def ml_contest_edit(request):
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
       
        if 1:
            image_bytes = base64.b64decode(result[11])  
            image = Image.open(io.BytesIO(image_bytes))
                
                # Resize the image to 300x300
            resized_image = image.resize((1200, 500))
            resized_image_bytes = io.BytesIO()
            resized_image.save(resized_image_bytes, format='PNG')
            data['image']= base64.b64encode(resized_image_bytes.getvalue()).decode('utf-8')
        else:
            1    
          
    return render(request,"ml_contest_edit.html",data)

def ml_contest_edited_info(request):  
    if request.method == 'POST':
        mydb,cursor = database()
        contestId = request.POST['contestId']
        try:
            text = request.POST['title']
            c = "update ml_contest set Title = '{}' where Id = '{}'".format(text,contestId)
            cursor.execute(c)
            mydb.commit()
        except:
            1    
        try:
            image = request.FILES['banner']
            print(image)
            image_base64 = base64.b64encode(image.read()).decode('utf-8')
           
            c = "update ml_contest set Banner = '{}' where Id = '{}'".format(image_base64,contestId)
            cursor.execute(c)
            mydb.commit()
        except:
            1            
        try:
            text = request.POST['contestDate']
            c = "update ml_contest set Contest_Date = '{}' where Id = '{}'".format(text,contestId)
            cursor.execute(c)
            mydb.commit()
        except:
            1   
        try:
            text = request.POST['contestFee']
            c = "update ml_contest set Contest_Fee = '{}' where Id = '{}'".format(text,contestId)
            cursor.execute(c)
            mydb.commit()
        except:
            1              
        try:
            text = request.POST['registrationDate']
            c = "update ml_contest set Registration_Last_Date = '{}' where Id = '{}'".format(text,contestId)
            cursor.execute(c)
            mydb.commit()
        except:
            1     
        try:
            text = request.POST['contestTime']
            c = "update ml_contest set Contest_Time = '{}' where Id = '{}'".format(text,contestId)
            cursor.execute(c)
            mydb.commit()
        except:
            1     
        try:
            text = request.POST['aboutContest']
            c = "update ml_contest set About_Contest = '{}' where Id = '{}'".format(text,contestId)
            cursor.execute(c)
            mydb.commit()
        except:
            1                
        try:
            text = request.POST['aboutDataset']
            c = "update ml_contest set About_Dataset = '{}' where Id = '{}'".format(text,contestId)
            cursor.execute(c)
            mydb.commit()
        except:
            1    
        try:
            text = request.POST['submissionGuideLine']
            c = "update ml_contest set Submission_Guideline = '{}' where Id = '{}'".format(text,contestId)
            cursor.execute(c)
            mydb.commit()
        except:
            1                                                                 
        data = dict()
        c = "select * from ml_contest where Id = '{}'".format(contestId)
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
        if 1:
            image_bytes = base64.b64decode(result[11])  
            image = Image.open(io.BytesIO(image_bytes))
                
                # Resize the image to 300x300
            resized_image = image.resize((1200, 500))
            resized_image_bytes = io.BytesIO()
            resized_image.save(resized_image_bytes, format='PNG')
            data['image']= base64.b64encode(resized_image_bytes.getvalue()).decode('utf-8')
        else:
            1            
    return render(request,"ml_contest_edit.html",data)

def ml_contest_registration(request):
        contest_id = request.GET.get('contestId')
        mydb,cursor=database()
        c="select About_Contest,Contest_Fee,Contest_Date,Registration_Last_Date,Banner,Title from ml_contest where Id = '{}'".format(contest_id)
        cursor.execute(c)
        result=cursor.fetchone()
        
        data = dict()
        data['contest_id'] = contest_id
        data['title'] = result[5]
        data['about_contest'] = result[0]
        data['fee']=result[1]
        data['contestDate']=result[2]
        data['registrationDate']=result[3]
        try:
            image_bytes = base64.b64decode(result[4])  
            image = Image.open(io.BytesIO(image_bytes))
                
            resized_image = image.resize((1200, 500))
            resized_image_bytes = io.BytesIO()
            resized_image.save(resized_image_bytes, format='PNG')
            data['image']= base64.b64encode(resized_image_bytes.getvalue()).decode('utf-8')   
        except:
            1         
        
        return render(request,"ml_contest_registration.html",data)

def ml_contest_registration_successfull(request):
    if request.method=="POST":
        contestId=request.POST['contestId']
        teamType=request.POST['teamType']
        teamName=request.POST['teamName']
        transaction=request.POST['transaction']
        paymentNumber=request.POST['paymentNumber']
        paymentType=request.POST['payment']
        name1 = email1 = mobile1 = ''
        name2 = email2 = mobile2 = ''
        name3 = email3 = mobile3 = ''
        
        if teamType == '1':
            name1 = request.POST['name1']
            email1 = request.POST['email1']
            mobile1 = request.POST['mobile1']
        elif teamType == '2':
            name1 = request.POST['name1']
            email1 = request.POST['email1']
            mobile1 = request.POST['mobile1']    
            name2 = request.POST['name2']
            email2 = request.POST['email2']
            mobile2  = request.POST['mobile2']
        elif teamType == '3':
            name1 = request.POST['name1']
            email1 = request.POST['email1']
            mobile1 = request.POST['mobile1']    
            name2 = request.POST['name2']
            email2 = request.POST['email2']
            mobile2  = request.POST['mobile2']      
            name3 = request.POST['name3']
            email3 = request.POST['email3']
            mobile3  = request.POST['mobile3']   
        
        mydb,cursor= database()
        current_datetime = datetime.now()

        datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        
        c="insert into ml_participant values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(contestId,teamName,teamType,paymentType,paymentNumber,transaction,name1,email1,mobile1,name2,email2,mobile2,name3,email3,mobile3,datetime_str,"Pending", 0.00,0,"")
        cursor.execute(c)
        mydb.commit()
            
    return render(request,"Landing_Page.html")
def imageMaker(image):
    try:
        image_bytes = base64.b64decode(image)  
        image = Image.open(io.BytesIO(image_bytes))

        resized_image = image.resize((150,150))
        resized_image_bytes = io.BytesIO()
        resized_image.save(resized_image_bytes, format='PNG')
        image= base64.b64encode(resized_image_bytes.getvalue()).decode('utf-8')
        return image
    except:
        return ''    
def ml_contest_team(contestId):
        data=dict()
        data['contestId']=contestId
        mydb,cursor=database()
        c="select Title,Contest_Fee from ml_contest where Id = '{}'".format(contestId)
        cursor.execute(c)
        result=cursor.fetchone()
        data['title']=result[0]
        data['fee']=result[1]
        c="select * from ml_participant where Contest_Id='{}'".format(contestId)
        cursor.execute(c)
        result = cursor.fetchall()
        
        teams = []
        counter =1
        for x in result:
            c="select Profile_Pic from user_info where Email='{}'".format(x[7])
            cursor.execute(c)
            img1 = cursor.fetchone()
            
            c="select Profile_Pic from user_info where Email='{}'".format(x[10])
            cursor.execute(c)
            img2 = cursor.fetchone()
            
            c="select Profile_Pic from user_info where Email='{}'".format(x[13])
            cursor.execute(c)
            img3 = cursor.fetchone()
            
            try:
                img1 = imageMaker(img1[0])
            except:
                1  
            try:
                img2 = imageMaker(img2[0])
            except:
                1      
            try:
                img3 = imageMaker(img3[0])
            except:
                1    
            team = {
                'serial' : counter,
                'id' : x[0],
                'teamName' : x[1],
                'teamMember': x[2],
                'paymentType': x[3],
                'accountNumber': x[4],
                'transaction' : x[5],
                'name1' : x[6],
                'email1': x[7],
                'mobile1': x[8],
                'name2' : x[9],
                'email2': x[10],
                'mobile2': x[11],  
                'name3' : x[12],
                'email3': x[13],
                'mobile3': x[14], 
                'rDateTime': x[15],
                'status' : x[16],  
                'img1' : img1,   
                'img2' : img2,   
                'img3' : img3,   
                
            }
            teams.append(team)
            counter = counter + 1
        data['teams'] = teams 
        return data   

def ml_contest_add_participant(request):
    data=dict()
    if request.method=="POST":
        contestId=request.POST['contestId']
        data = ml_contest_team(contestId)
           
    return render(request,"ml_contest_add_participant.html",data)

def ml_contest_registration_approved(request):
    if request.method=='POST':
        data = dict()
        contestId=request.POST['contestId']
        email=request.POST['email']
        name=request.POST['name']
        
        data['contestId']=contestId
        mydb,cursor = database()
        data = ml_contest_team(contestId) 
        c="select Status from ml_participant where Contest_Id = '{}' and Email1 = '{}'".format(contestId,email)
        cursor.execute(c)
        result=cursor.fetchone()
        
        if result[0]=="Pending": 
            c="update ml_participant set Status = '{}' where Contest_Id = '{}' and Email1 = '{}'".format("Approved",contestId,email)
            cursor.execute(c)
            mydb.commit()
        
            sender = "mlcodeverse@gmail.com"
            receiver = email
            current_datetime = datetime.now()
            datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            header = "Contest Request Approval"
            message = "Congratulations "+name+", Your request to participate in the contest "+ data['title'] + "has been approved. Stay with us, and we will provide you with a contest pass key shortly."
            
            c="insert into message values('{}','{}','{}','{}','{}')".format(sender,receiver,datetime_str,header,message)
            cursor.execute(c)
            mydb.commit()
        else:
            c="update ml_participant set Status = '{}' where Contest_Id = '{}' and Email1 = '{}'".format("Pending",contestId,email)
            cursor.execute(c)
            mydb.commit()
        
            sender = "mlcodeverse@gmail.com"
            receiver = email
            current_datetime = datetime.now()
            datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            header = "Contest Request Approval"
            message = "Congratulations "+name+", Your request to participate in the contest "+ data['title'] + "has been approved. Stay with us, and we will provide you with a contest pass key shortly."
            
            c="insert into message values('{}','{}','{}','{}','{}')".format(sender,receiver,datetime_str,header,message)
            cursor.execute(c)
            mydb.commit()
            
        data = ml_contest_team(contestId) 
       
      
    return render(request,"ml_contest_add_participant.html",data)   

def oraganizational_dashboard(request):
    current_user=request.user
    username=current_user.username
    
    data = dict()
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
    
  
    return render(request,"organization_dashboard.html",data)


def ml_leaderboard_data(contest_id):
    mydb,cursor=database()
    c="select Team,Accuracy,Email1,Email2,EMail3,NumberOfEntry,LastSubmit from ml_participant where Contest_Id='{}' and Accuracy!='{}' order by Accuracy desc, LastSubmit asc limit 20".format(contest_id,0.0)
    cursor.execute(c)
    result = cursor.fetchall()
    teams=[]
    i=1
    for x in result:
        img1=img2=img3=''
        name1=name2=name3=''
        try:
            c="select Profile_Pic,Name from user_info where Email = '{}'".format(x[2])
            cursor.execute(c)
            img = cursor.fetchone()
            img1 = imageMaker(img[0])
            name1=img[1]
           
        except:
            1
                
        try:
            c="select Profile_Pic,Name from user_info where Email = '{}'".format(x[3])
            cursor.execute(c)
            img = cursor.fetchone()
            img2 = imageMaker(img[0])
            name2=img[1]

        except:
         1
        
        try:
            c="select Profile_Pic,Name from user_info where Email = '{}'".format(x[4])
            cursor.execute(c)
            img = cursor.fetchone()
            img3 = imageMaker(img[0])
            name3=img[1]
            
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
            'img3': img3,
            'email1': x[2],
            'email2': x[3],
            'email3': x[4],
            'name1': name1,
            'name2': name2,
            'name3': name3
        }
        i=i+1
        teams.append(team)
    return teams
def mlContestDetails(request):
    if request.method=="POST":
        contestId = request.POST['contest-id']
        mydb,cursor=database()
        c="select count(Contest_Id), sum(NumberOfEntry) from ml_participant where Contest_Id = '{}'".format(contestId)
        cursor.execute(c)
        result = cursor.fetchone()
        data = dict()
        data['teams'] = ml_leaderboard_data(contestId)
        data['team']=result[0]
        data['submit']=result[1]
        
        c="select max(Accuracy), min(Accuracy) from ml_participant where Contest_Id = '{}' and NumberOfEntry != '{}'".format(contestId,0)
        cursor.execute(c)
        result = cursor.fetchone()
        data['max']=result[0]
        data['min']=result[1]
        data['cid']=contestId
        
        c="select Title from ml_contest where Id='{}'".format(contestId)
        cursor.execute(c)
        result=cursor.fetchone()
        data['contestTitle'] = result[0]
    return render(request,"ml_contest_details.html",data)
            