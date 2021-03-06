from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from rest_framework.response import Response
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Enroll_Data,Student,Marksheet

# Create your views here.
def logout(request):
    auth.logout(request)
    return redirect('/')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('addstudent')
        else:
            messages.info(request,"Invalid Credentials !!")
            return redirect('/adminlogin')
    else:
        return render(request,'login.html')

import xlrd
import pandas as pd
def addstudent(request):
    if request.method == 'POST':
        file = request.FILES.get('enroll_list')
        enroll_Data = Enroll_Data.objects.create(enroll_datasheet = file)
        enroll_datasheet_path = enroll_Data.enroll_datasheet.path
        
        '''
        wb = xlrd.open_workbook(enroll_datasheet_path)
        sheet = wb.sheet_by_index(0)
        print(sheet.nrows)
        for i in range(1,sheet.nrows):
            enroll=sheet.cell_value(i,0)
            name=sheet.cell_value(i,2)
            branch=sheet.cell_value(i,4)
            section=sheet.cell_value(i,6)
            student = Student.objects.create(enrollment = enroll,name=name,section=section,branch=branch)
        print("hello")    
        return render(request,'admindashboard/addstudent.html',{'message':'Data Saved Successfully'})'''
        import pandas as pd
        df = pd.read_excel (enroll_datasheet_path)
        print(df)
        for i in df.itertuples():
            enroll=i[1]
            name=i[3]
            branch=i[5]
            section=i[7]
            student = Student.objects.create(enrollment = enroll,name=name,section=section,branch=branch)
        return render(request,'admindashboard/addstudent.html',{'message':'Data Saved Successfully'})
    else:
        return render(request,'admindashboard/addstudent.html')



def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('register')
            else:
                user =User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                return redirect('login')
        else:
            messages.info(request,'Password not matched')
            return redirect('register')
    else:
        return render(request,'register.html')

def updatemarksheet(request):
    return render(request,'admindashboard/uploadmarksheet.html')

def updatereceipt(request):
    return render(request,'admindashboard/uploadreceipt.html')
import json

def updatemarksheetdata(request):
    marksheet_data=json.loads(request.POST.get('dict'))
    semester=request.POST.get('sem')
    print(marksheet_data,semester)
    accept=[]
    reject=[]
    for i in marksheet_data:
        print(i)
        student=Student.objects.filter(enrollment=i)
        print(student)
        marksheet=Marksheet.objects.get_or_create(student_id=student[0])
        marksheet=marksheet[0]
        try:
            if(marksheet.marksheet_URL==None):
                print("in if")
                d={}
                d[semester]=marksheet_data[i]
                d_json=json.dumps(d)
                marksheet.marksheet_URL=d_json
                marksheet.save()
            else:
                print("in else")
                d=marksheet.marksheet_URL
                d_dict=json.loads(d)
                d_dict[semester]=marksheet_data[i]
                d_json=json.dumps(d_dict)
                marksheet.marksheet_URL=d_json
                marksheet.save()
            accept.append(i)
        except:
            reject.append(i)
    response={'accept':accept,'reject':reject}
    print(response)
    return HttpResponse(json.dumps(response))

def updatereceiptdata(request):
    receipt_data=json.loads(request.POST.get('dict'))
    semester=request.POST.get('sem')
    accept=[]
    reject=[]
    for i in receipt_data:
        student=Student.objects.filter(enrollment=i)
        receipt=Marksheet.objects.get_or_create(student_id=student[0])
        receipt=receipt[0]
        try:
            if(receipt.receipt_URL==None):
                print("in if")
                d={}
                d[semester]=receipt_data[i]
                d_json=json.dumps(d)
                receipt.receipt_URL=d_json
                receipt.save()
            else:
                print("in else")
                d=receipt.receipt_URL
                d_dict=json.loads(d)
                d_dict[semester]=receipt_data[i]
                d_json=json.dumps(d_dict)
                receipt.receipt_URL=d_json
                receipt.save()
            accept.append(i)
        except:
            reject.append(i)
    response={'accept':accept,'reject':reject}
    print(response)
    return HttpResponse(json.dumps(response))

def showstudent(request):
    student=Student.objects.all().order_by('-session','branch','name')
    return render(request,'admindashboard/showstudent.html',{'student':student})
