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
import subprocess
import os
import math
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
def Host_Programming_Contest(request):
    current_user=request.user
    username=current_user.username
    data = dict()
    mydb,cursor = database()

    if request.method == 'POST':
        if 1:
            contest_title = request.POST['contest_title']
            contest_description = request.POST['contest_description']
            rules = request.POST['rules']
            contest_date_time = request.POST['contest_date_time']
            contest_fee = request.POST['contest_fee']
            registration_date = request.POST['registration_date']
          
            image = request.FILES['banner']
            image_base64 = base64.b64encode(image.read()).decode('utf-8')
   
            contest_date=contest_date_time[:10]
            contest_time=contest_date_time[11:]

            c="select count(Id) from programming_contest"
            cursor.execute(c)
            result = cursor.fetchone()
            contestId= result[0] + 1
            
            current_date = datetime.now()
            current_month = current_date.month
            current_year = current_date.year
            current_day =current_date.day
                    
            date=str(current_year)+'-'+str(current_month)+'-'+str(current_day)
            date = str(date).replace('-', '')
           
            contestId='contest_id'+date[2:]+str(contestId)
            c="insert into programming_contest values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(contestId,contest_title,contest_description,rules,contest_date,contest_time,contest_fee,registration_date,username,"Pending",image_base64)  
            cursor.execute(c)
            mydb.commit()
        else:
            1    
        return redirect('Programming_Contest_List')        
    return render(request,"host_programming_contest.html")

def Programming_contest_list(request):
    current_user=request.user
    username=current_user.username
    data = dict()
    mydb,cursor = database()
  
    if len(username) != 0:
        c = " select * from programming_contest where Author_Id = '{}' order by Contest_Date".format(username)
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
                'status' : x[9]
            }
            counter = counter + 1
            contest_list.append(contest)
        data['contest_list']=contest_list  

    return render(request,"programming_contest_list.html", data)

def contest_info(contestId):
        mydb,cursor = database()
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
        data['contestDate']=cDate
        data['contestTime']=result[5]
        data['contestFee']=result[6]
        data['registrationDate']=rDate
       
        if 1:
            image_bytes = base64.b64decode(result[10])  
            image = Image.open(io.BytesIO(image_bytes))
                
          
            resized_image = image.resize((1200, 500))
            resized_image_bytes = io.BytesIO()
            resized_image.save(resized_image_bytes, format='PNG')
            data['image']= base64.b64encode(resized_image_bytes.getvalue()).decode('utf-8')
        else:
            1 
        return data       

def Programming_Contest_Edit(request):
    if request.method == 'POST':
        contestId = request.POST['contestId']
        data=dict()
        data=contest_info(contestId)      
    return render(request,"programming_contest_edit.html",data)


def programming_contest_edited_info(request):  
    if request.method == 'POST':
        mydb,cursor = database()
        contestId = request.POST['contestId']
        try:
            text = request.POST['title']
            c = "update programming_contest set Title = '{}' where Id = '{}'".format(text,contestId)
            cursor.execute(c)
            mydb.commit()
        except:
            1    
        try:
            image = request.FILES['banner']
            print(image)
            image_base64 = base64.b64encode(image.read()).decode('utf-8')
           
            c = "update programming_contest set Banner = '{}' where Id = '{}'".format(image_base64,contestId)
            cursor.execute(c)
            mydb.commit()
        except:
            1            
        try:
            text = request.POST['contestDate']
            c = "update  programming_contest set Contest_Date = '{}' where Id = '{}'".format(text,contestId)
            cursor.execute(c)
            mydb.commit()
        except:
            1   
        try:
            text = request.POST['contestFee']
            c = "update programming_contest set Contest_Fee = '{}' where Id = '{}'".format(text,contestId)
            cursor.execute(c)
            mydb.commit()
        except:
            1              
        try:
            text = request.POST['registrationDate']
            c = "update  programming_contest set Registration_Last_Date = '{}' where Id = '{}'".format(text,contestId)
            cursor.execute(c)
            mydb.commit()
        except:
            1     
        try:
            text = request.POST['contestTime']
            c = "update  programming_contest set Contest_Time = '{}' where Id = '{}'".format(text,contestId)
            cursor.execute(c)
            mydb.commit()
        except:
            1     
        try:
            text = request.POST['aboutContest']
            c = "update  programming_contest set About_Contest = '{}' where Id = '{}'".format(text,contestId)
            cursor.execute(c)
            mydb.commit()
        except:
            1
        try:                                                     
            data = dict()
            data=contest_info(contestId)   
        except:
            1           
    return render(request,"programming_contest_edit.html",data)
    
def programming_contest_registration(request):
        contest_id = request.GET.get('contestId')
        mydb,cursor=database()
        c="select About_Contest,Contest_Fee,Contest_Date,Registration_Last_Date,Banner,Title from programming_contest where Id = '{}'".format(contest_id)
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
        
        return render(request,"programming_contest_registration.html",data)    

def programming_contest_registration_successfull(request):
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
        
        c="insert into programming_participant values ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(contestId,teamName,teamType,paymentType,paymentNumber,transaction,name1,email1,mobile1,name2,email2,mobile2,name3,email3,mobile3,datetime_str,"Pending")
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
      
def programming_contest_team(contestId):
        data=dict()
        data['contestId']=contestId
        mydb,cursor=database()
        c="select Title,Contest_Fee from programming_contest where Id = '{}'".format(contestId)
        cursor.execute(c)
        result=cursor.fetchone()
        data['title']=result[0]
        data['fee']=result[1]
        c="select * from programming_participant where Contest_Id='{}'".format(contestId)
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

def programming_contest_add_participant(request):
    data=dict()
    if request.method=="POST":
        contestId=request.POST['contestId']
        data = programming_contest_team(contestId)
           
    return render(request,"programming_contest_add_participant.html",data)

def programming_contest_registration_approved(request):
    if request.method=='POST':
        data = dict()
        contestId=request.POST['contestId']
        email=request.POST['email']
        name=request.POST['name']
        
        data['contestId']=contestId
        mydb,cursor = database()
        data = programming_contest_team(contestId) 
        c="select Status from programming_participant where Contest_Id = '{}' and Email1 = '{}'".format(contestId,email)
        cursor.execute(c)
        result=cursor.fetchone()
        
        if result[0]=="Pending": 
            c="update programming_participant set Status = '{}' where Contest_Id = '{}' and Email1 = '{}'".format("Approved",contestId,email)
            cursor.execute(c)
            mydb.commit()
        
            sender = "daffodil@diu.edu.bd"
            receiver = email
            current_datetime = datetime.now()
            datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            header = "Contest Request Approval"
            message = "Congratulations "+name+", Your request to participate in the contest "+ data['title'] + "has been approved. Stay with us, and we will provide you with a contest pass key shortly."
            
            c="insert into message values('{}','{}','{}','{}','{}')".format(sender,receiver,datetime_str,header,message)
            cursor.execute(c)
            mydb.commit()
        else:
            c="update programming_participant set Status = '{}' where Contest_Id = '{}' and Email1 = '{}'".format("Pending",contestId,email)
            cursor.execute(c)
            mydb.commit()
        
            sender = "daffodil@diu.edu.bd"
            receiver = email
            current_datetime = datetime.now()
            datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
            header = "Contest Request Approval"
            message = "Congratulations "+name+", Your request to participate in the contest "+ data['title'] + "has been approved. Stay with us, and we will provide you with a contest pass key shortly."
            
            c="insert into message values('{}','{}','{}','{}','{}')".format(sender,receiver,datetime_str,header,message)
            cursor.execute(c)
            mydb.commit()
                
        data = programming_contest_team(contestId) 
       
      
    return render(request,"programming_contest_add_participant.html",data)   

def create_Problemset(request):
    data=dict()
    if request.method=='POST':
        contestId = request.POST['contestId']
       
        mydb,cursor = database()
        c="select Title from programming_contest where Id = '{}'".format(contestId)
        cursor.execute(c)
        result = cursor.fetchone()
        data['contestId'] = contestId
        data['title']=result[0]
        try:
            serial = request.POST['serial']
            title = request.POST['title']
            problemDescription = request.POST['problem-description']
            inputDescription = request.POST['input-description']
            outputDescription = request.POST['output-description']
            argNumber = request.POST['num-argument']
            argType = request.POST['argument-type']
            csv_file = request.FILES['csv_file'].read().decode('utf-8').splitlines()
            reader = csv.reader(csv_file)
            csv_data = [row for row in reader]
            
            c="select count(Problem_Id) from programming_contest_problemset where Contest_Id='{}'".format(contestId)
            cursor.execute(c)
            result=cursor.fetchone()
            problemId=contestId + str(int(result[0])+1)
            
            c="insert into programming_contest_problemset values ('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(contestId,problemId,title,problemDescription,inputDescription,outputDescription,argNumber,argType,serial)
            cursor.execute(c)
            mydb.commit()
            counter = 0
            for x in csv_data:
                counter = counter + 1
                if counter==1:
                    continue
                if argNumber=='1':
                    c = "INSERT INTO singleLineInputTestCase VALUES ('{}', '{}','{}')".format(problemId, x[0], x[1])
                    cursor.execute(c)
                    mydb.commit()
        except:
            1    
            
    return render(request,"create_problemset.html",data)
   
def programming_contest_home(request):
    if request.method=="GET":
        try:
            contestId=request.GET['contestId']
            current_user=request.user
            email=current_user.username
        
            mydb,cursor=database()
            data = dict()
            c = "select * from programming_contest where Id = '{}'".format(contestId)
            cursor.execute(c)
            result = cursor.fetchone()
            
            data['uid']=email
            data['contestId']=contestId
            data['title']=result[1]
            data['aboutContest']=result[2]
            data['rules']=result[3]
            data['contestDate']=result[4]
            data['contestTime']=result[5]

        
            image_bytes = base64.b64decode(result[10])  
            image = Image.open(io.BytesIO(image_bytes))

            resized_image = image.resize((1200, 500))
            resized_image_bytes = io.BytesIO()
            resized_image.save(resized_image_bytes, format='PNG')
            data['image']= base64.b64encode(resized_image_bytes.getvalue()).decode('utf-8')
            
            c="select Problem_Id,Problem_Title,Serial from programming_contest_problemset where Contest_Id = '{}'".format(contestId)
            cursor.execute(c)
            result=cursor.fetchall()
            
            problems = []
            for x in result:
                problem={
                    'id': x[0],
                    'title': x[1],
                    'serial': x[2]
                }
                problems.append(problem)
            data['problems']=problems    
            data['pic']=userProfilePic(email) 
        except:
            1   
            
        c="select Contest_Id from programming_participant where Contest_Id = '{}' and Status != '{}' and (Email1= '{}' or Email2='{}' or Email3='{}')".format(contestId,'Pending',email,email,email)
        cursor.execute(c)
        result=cursor.fetchone()
        try:
            flag = len(result[0])
        except:
            flag=0     
            data['cid'] = '1'
 
    return render(request,"programming_contest_home.html",data)
def problemInfo(problemId):
        data=dict()
        mydb,cursor=database()
        c="select * from programming_contest_problemset where Problem_Id = '{}'".format(problemId)
        cursor.execute(c)
        result=cursor.fetchone()
        
        data['problemId'] = problemId
        data['title']=result[2]
        data['description']=result[3]
        data['input']=result[4]
        data['output']=result[5]
        
        c="select * from singlelineinputtestCase where Problem_Id='{}' limit 3".format(problemId)
        cursor.execute(c)
        result=cursor.fetchall()
        testcases=[]
        for x in result:
            testcase={
                'input': x[1],
                'output':x[2]
            }
            testcases.append(testcase)
        data['testcases']=testcases  
        return data

def contestProblems(request):
    data=dict()
    data['authenticate'] = 0
    if request.method=="POST":
        problemId=request.POST['problemId']
        contestId = request.POST['contest-id']
    
        mydb,cursor =database()
               
        current_user=request.user
        email=current_user.username
        c="select Contest_Id from programming_participant where Contest_Id='{}' and (Email1='{}' or Email2='{}' or Email3='{}')".format(contestId,email,email,email)
        cursor.execute(c)
        contest = cursor.fetchone()
        if contest:
            data = problemInfo(problemId)
            data['state'] = 0
            data['contestId']=contestId
            data['authenticate'] = 1
            data['pic']=userProfilePic(email) 
            try:
                c="select SubmittedCode from programming_contest_leaderboard where problemId = '{}' and (Email1='{}' or Email2='{}' or Email3='{}')".format(problemId,email,email,email)
                cursor.execute(c)
                code = cursor.fetchone()
                data['code']=code[0]
            except:
                1    
        c="select Contest_Id from programming_participant where Contest_Id = '{}' and Status != '{}' and (Email1= '{}' or Email2='{}' or Email3='{}')".format(contestId,'Pending',email,email,email)
        cursor.execute(c)
        result=cursor.fetchone()
        try:
            flag = len(result[0])
        except:
            flag=0     
            data['cid'] = '1'
    return render(request,"programming_contest_problem.html",data)



def execute_c_code(c_code, inputs):
    output = []
    # Temporary file names
    temp_c_file = "temp_program.c"
    executable_file = "program_executable"

    try:
        # Step 1: Save the submitted C code to a temporary file
        with open(temp_c_file, "w") as file:
            file.write(c_code)

        # Step 2: Compile the C code
        compile_cmd = ["gcc", temp_c_file, "-o", executable_file]
        compile_process = subprocess.run(compile_cmd, capture_output=True, text=True)

        # Check for compilation errors
        if compile_process.returncode != 0:
            raise Exception(f"Compilation failed:\n{compile_process.stderr}")

        # If on Windows, adjust the executable file name
        if os.name == 'nt':  # Windows OS
            executable_file += ".exe"

        # Step 3: Execute the compiled program for each input
        for input_data in inputs:
            try:
                # Run the executable with the input
                run_process = subprocess.run(
                    ["./" + executable_file],
                    input=input_data + "\n",  # Ensure newline is passed for input
                    capture_output=True,
                    text=True,
                    check=True
                )

                # Collect the output
                output.append(run_process.stdout.strip())

            except subprocess.CalledProcessError as e:
                output.append(f"Error executing program for input '{input_data}': {e.stderr.strip()}")

    finally:
        # Cleanup temporary files
        if os.path.exists(temp_c_file):
            os.remove(temp_c_file)
        if os.path.exists(executable_file):
            os.remove(executable_file)

    return output


def run_code(request):
    if request.method == "POST":
        submitted_c_code = request.POST.get('code', '')
        problem_id = request.POST['problem-id']
        contestId = request.POST['contest-id']
        mydb,cursor = database()
        c="select Input,Output from singlelineinputtestcase where Problem_Id = '{}'".format(problem_id)
        cursor.execute(c)
        testcase = cursor.fetchall()
        

        test_inputs = []
        test_outputs = []
        
        for x in testcase:
            test_inputs.append(str(x[0]))
            test_outputs.append(str(x[1]))

        try:
            result = execute_c_code(submitted_c_code, test_inputs)
        except Exception as e:
            result = [str(e)]
        data = dict()
        
        data = problemInfo(problem_id)
        data['contestId']=contestId
        data['authenticate'] = 1
        solution = []
        
        counter = 0
        try:
            for x in range(0,3):
                if test_outputs[counter]==result[counter]:
                    solution.append("True")
                else:
                    solution.append("False")    
                counter=counter+1
                
            data['result'] =solution
            data['expected'] = test_outputs
            data['input1']=test_inputs[0]
            data['input2']=test_inputs[1]
            data['input3']=test_inputs[2]
            
            data['output1']=result[0]
            data['output2']=result[1]
            data['output3']=result[2]
    
            
            data['expected1']=test_outputs[0]
            data['expected2']=test_outputs[1]
            data['expected3']=test_outputs[2]
            
            data['status1']=solution[0]
            data['status2']=solution[1]
            data['status3']=solution[2]
            data['code'] = submitted_c_code
            data['state'] = 1
        except:
            data['error'] = result   
            data['code'] = submitted_c_code 
                    
        current_user=request.user
        email=current_user.username
        data['pic']=userProfilePic(email) 
        c="select Contest_Id from programming_participant where Contest_Id = '{}' and Status != '{}' and (Email1= '{}' or Email2='{}' or Email3='{}')".format(contestId,'Pending',email,email,email)
        cursor.execute(c)
        result=cursor.fetchone()
        try:
            flag = len(result[0])
        except:
            flag=0     
            data['cid'] = '1'
       
    return render(request, "programming_contest_problem.html", data)

def submit_code(request):
    if request.method=="POST":
        submitted_c_code = request.POST.get('code', '')
        problem_id = request.POST['problem-id']
        contestId = request.POST['contest-id']
        mydb,cursor = database()
        c="select Input,Output from singlelineinputtestcase where Problem_Id = '{}'".format(problem_id)
        cursor.execute(c)
        testcase = cursor.fetchall()
        
        current_user=request.user
        email=current_user.username

        test_inputs = []
        test_outputs = []
        
        for x in testcase:
            test_inputs.append(str(x[0]))
            test_outputs.append(str(x[1]))

        try:
            result = execute_c_code(submitted_c_code, test_inputs)
        except Exception as e:
            result = [str(e)]
        data = dict()
      
        data = problemInfo(problem_id)
        data['contestId']=contestId
        solution = []
        
        counter = 0
        passTest = 0
        failTest = 0
        totalTest = len(testcase)
        try:
            for x in result:
                if test_outputs[counter]==x:
                    solution.append("True")
                    passTest = passTest + 1
                else:
                    solution.append("False")   
                    failTest = failTest + 1 
                counter=counter+1
                
            data['result'] =solution
            data['expected'] = test_outputs
            data['input1']=test_inputs[0]
            data['input2']=test_inputs[1]
            data['input3']=test_inputs[2]
            
            data['output1']=result[0]
            data['output2']=result[1]
            data['output3']=result[2]
    
            
            data['expected1']=test_outputs[0]
            data['expected2']=test_outputs[1]
            data['expected3']=test_outputs[2]
            
            data['status1']=solution[0]
            data['status2']=solution[1]
            data['status3']=solution[2]
            data['code'] = submitted_c_code
            data['state'] = 1
            data['submission'] = 1
            
            data['totalTestCase'] = passTest + failTest
            data['passTest'] = passTest
            data['failTest'] = failTest
        except:
            data['error'] = result   
            data['code'] = submitted_c_code    
        
        status = 0
        if totalTest == passTest:
            status = 1
        
        
        c="select Team,Email1,Email2,Email3 from programming_participant where Contest_Id = '{}' and ( Email1='{}' or Email2='{}' or Email3='{}')".format(contestId,email,email,email);   
        cursor.execute(c)
        team = cursor.fetchone()
        team_Name = team[0]
        email1 = team[1]
        email2 = team[2]
        email3 = team[3]
        
        numberOfSubmission = 0
        c="select  NumberOfSubmission from programming_contest_leaderboard where  problemId = '{}' and (Email1 = '{}' or Email2='{}' or Email3='{}')".format(problem_id,email,email,email)
        cursor.execute(c)
        submissionCount = cursor.fetchone()
        if submissionCount:
            numberOfSubmission = int(submissionCount[0]) + 1
        else:
            numberOfSubmission = 0        
          
        current_datetime = datetime.now()
        time_str = str(current_datetime.strftime("%H:%M:%S"))
        print("hello i am l uploading ")
        if numberOfSubmission == 0:
            c="insert into programming_contest_leaderboard values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(problem_id,contestId,team_Name,email1,email2,email3,1,status,time_str,submitted_c_code)
            cursor.execute(c)
            mydb.commit()   
        else:
            c="update programming_contest_leaderboard set NumberOfSubmission = '{}', ProblemStatus='{}', SubmissionTime='{}', SubmittedCode='{}' where problemId='{}' and (Email1='{}' and Email2='{}' and Email3='{}')".format(numberOfSubmission,status,time_str,submitted_c_code,problem_id,email1,email2,email3)
            cursor.execute(c)
            mydb.commit()  
        data['email1']=email1
        data['email2']=email2
        data['email3']=email3   
        data['authenticate'] = 1 
        print("hello i am submit")
        data['pic']=userProfilePic(email)     
        c="select Contest_Id from programming_participant where Contest_Id = '{}' and Status != '{}' and (Email1= '{}' or Email2='{}' or Email3='{}')".format(contestId,'Pending',email,email,email)
        cursor.execute(c)
        result=cursor.fetchone()
        try:
            flag = len(result[0])
        except:
            flag=0     
            data['cid'] = '1'
       
    return render(request, "programming_contest_problem.html", data)

def programming_leaderboard(request):
    if request.method == "POST":
        mydb,cursor = database()
        contestId = request.POST['contestId']

        
        c="select Contest_Time from programming_contest where Id='{}'".format(contestId)
        cursor.execute(c)
        contestTime = cursor.fetchone()
        cTime = str(contestTime[0])
        cHour = int(cTime[:2])
        cMin = int(cTime[3:5])
        cSec = int(cTime[6:])
        
        if cHour == 0:
            cHour = 24
        cTime = cHour*60*60 + cMin*60 + cSec
        count = 0
        c="select Team,Email1,Email2,Email3 from programming_participant where Contest_Id = '{}'".format(contestId)
        cursor.execute(c)
        teamInfo = cursor.fetchall()
        
        data = dict()
      
        teams = []
        for x in teamInfo:
            c="select Problem_Id,Serial from programming_contest_problemset where Contest_Id = '{}'  order by Serial asc".format(contestId)
            cursor.execute(c)
            problems = cursor.fetchall()
            problemStatus = []
            count = count + 1
            score = 0
            totalSubmission = 0
            for problem in problems:
                c="select NumberOfSubmission,ProblemStatus,SubmissionTime from programming_contest_leaderboard where ContestId='{}' and ProblemId= '{}' and (Email1='{}' or Email2='{}' or Email3='{}')".format(contestId,problem[0], x[1],x[2],[3])
                cursor.execute(c)
                result = cursor.fetchone()
              
                
                try:
                    time_str = str(result[2])
                    try:
                    
                        hour=int(time_str[0:2])
                    except:
                        hour =int(time_str[0:1])
                    try:     
                        min=int(time_str[3:5])
                    except:
                        min=int(time_str[3:4])  
                    try:      
                        sec=int(time_str[6:])
                    except:
                        sec= int(time_str[5:])  
                        
                    if hour==0:
                        hour=24
                    time=hour*60*60 + min*60 + sec
                    time = time  -  cTime  
                    time = math.ceil(time/60)
                except:
                    time = ''
                        
                    

                try:    
                    problemresult = {
                        'status' : result[1],
                        'numberOfsubmit' : result[0],
                        'time' : time,
                        'serial': problem[1]
                        }
                    problemStatus.append(problemresult)
                except:
                    problemresult = {
                        'status' : '',
                        'numberOfsubmit' : '',
                        'time' : '',
                        'serial': problem[1]
                        }
                    problemStatus.append(problemresult)
                try:
                    score = score + int(time)
                except: 
                    score = score  
                if problemresult['status'] == '1':
                    totalSubmission = totalSubmission + 1  
                          
            team ={
                'serial': count,
                "teamName" : x[0],
                'email1': x[1],
                'email2': x[2],
                'email3': x[3],
                'score' : score,
                'totalSubmission' : totalSubmission,
                'solutions': problemStatus
            }
            teams.append(team)

        data['teams'] = sorted(teams, key=lambda x: (-x['totalSubmission'], x['score']))
        data['contestId'] = contestId
        
        current_user=request.user
        email=current_user.username
        data['pic']=userProfilePic(email) 
        
        c="select Problem_Id,Problem_Title,Serial from programming_contest_problemset where Contest_Id='{}'".format(contestId)
        cursor.execute(c)
        result=cursor.fetchall()
        problems = []
        for x in result:
            c="select count(ProblemStatus) from programming_contest_leaderboard where problemId='{}' and ProblemStatus='{}'".format(x[0],1)
            cursor.execute(c)
            solved = cursor.fetchone()
            
            c="select count(ProblemStatus) from programming_contest_leaderboard where problemId='{}' and ProblemStatus='{}'".format(x[0],0)
            cursor.execute(c)
            wrong = cursor.fetchone()
            
            c="select sum(NumberOfSubmission) from programming_contest_leaderboard where problemId='{}'".format(x[0])
            cursor.execute(c)
            tried = cursor.fetchone()
            
            problem={
                'serial': x[2],
                'solved': solved[0],
                'total': str(int(solved[0])+int(wrong[0]))
            }
            problems.append(problem)
        data['problems'] = problems
    return render(request,"programming_leaderboard.html",data)

def programming_contest_details(request):
    if request.method == "POST":
        mydb,cursor = database()
        contestId = request.POST['contestId']
        data = dict()

        data['contestId'] = contestId
        c="select count(contest_Id) from programming_participant where contest_Id='{}'".format(contestId)
        cursor.execute(c)
        team=cursor.fetchone()
        data['totalTeam']=team[0]
        
        c="select Title from programming_contest where Id='{}'".format(contestId)
        cursor.execute(c)
        title =  cursor.fetchone()
        data['title'] = title[0]
        
            
        numberOfMember = 0
        c="select count(Email1) from programming_participant where contest_Id = '{}' and Email1 != '{}'".format(contestId,'')
        cursor.execute(c)
        member = cursor.fetchone()
        numberOfMember = numberOfMember + int(member[0])
        
        c="select count(Email2) from programming_participant where contest_Id = '{}' and Email2 != '{}'".format(contestId,'')
        cursor.execute(c)
        member = cursor.fetchone()
        numberOfMember = numberOfMember + int(member[0])
      
        c="select count(Email3) from programming_participant where contest_Id = '{}' and Email3 != '{}'".format(contestId,'')
        cursor.execute(c)
        member = cursor.fetchone()
        numberOfMember = numberOfMember + int(member[0])
        
        data['totalMember']=numberOfMember
        
        c="select count(contestId) from programming_contest_leaderboard where contestId = '{}' and ProblemStatus = '{}'".format(contestId,1)
        cursor.execute(c)
        correctSubmission = cursor.fetchone()
        data['correct']=correctSubmission[0]
        
        c="select count(contestId) from programming_contest_leaderboard where contestId = '{}' and ProblemStatus = '{}'".format(contestId,0)
        cursor.execute(c)
        correctSubmission = cursor.fetchone()
        data['wrong']=correctSubmission[0]
        
        
        c="select Problem_Id,Problem_Title,Serial from programming_contest_problemset where Contest_Id='{}'".format(contestId)
        cursor.execute(c)
        result=cursor.fetchall()
        
        problems = []
        for x in result:
            c="select count(ProblemStatus) from programming_contest_leaderboard where problemId='{}' and ProblemStatus='{}'".format(x[0],1)
            cursor.execute(c)
            solved = cursor.fetchone()
            
            c="select count(ProblemStatus) from programming_contest_leaderboard where problemId='{}' and ProblemStatus='{}'".format(x[0],0)
            cursor.execute(c)
            wrong = cursor.fetchone()
            
            c="select sum(NumberOfSubmission) from programming_contest_leaderboard where problemId='{}'".format(x[0])
            cursor.execute(c)
            tried = cursor.fetchone()
            
            problem={
                'id': x[0],
                'title': x[1],
                'serial': x[2],
                'solved': solved[0],
                'wrong': wrong[0],
                'try': tried[0],
                'total': str(int(solved[0])+int(wrong[0]))
            }
            problems.append(problem)
        data['problems']=problems
        
        
    return render(request,"programming_contest_details.html",data)
    
        
