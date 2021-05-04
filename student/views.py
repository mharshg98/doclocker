from django.shortcuts import render,HttpResponse,redirect
from Admin.models import Student,Marksheet
from django.contrib import messages
def login(request):
    return render(request,'studentlogin.html')
# Create your views here.

def redirect1(request):
    if request.method == 'POST':
        email=request.user.email
        enroll=request.POST.get('enrollment')
        mobile=request.POST.get('mobile')
        session=request.POST.get('session')
        student=Student.objects.filter(enrollment=enroll)
        if(len(student)>0):
            student=student[0]
            student.email=email
            student.session=session
            student.mobile=mobile
            student.save()
            return redirect('dashboard')
        else:
            return render(request,'studentdashboard/verify.html',{'flag':True}) 
    else:
        email=request.user.email
        student=Student.objects.filter(email=email)
        if(len(student)==0):
            return render(request,'studentdashboard/verify.html',{'flag':False})
        else:
            return redirect('dashboard')
import json
def dashboard(request):
    email=request.user.email
    student=Student.objects.filter(email=email)
    marksheet=Marksheet.objects.filter(student_id=student[0])
    if(len(marksheet)==0):
        return render(request,'studentdashboard/home.html',{'flag':False})
    else:
        d=json.loads(marksheet[0].marksheet_URL)
        sem=[]
        url=[]
        print(d)
        for i in sorted(d):
            sem.append(i)
            url.append(d[i])
        return render(request,'studentdashboard/home.html',{'flag':True,'sem_url':zip(sem, url)})

def receipt(request):
    email=request.user.email
    student=Student.objects.filter(email=email)
    marksheet=Marksheet.objects.filter(student_id=student[0])
    print(marksheet)
    if(len(marksheet)==0):
        return render(request,'studentdashboard/receipt.html',{'flag':False})
    else:
        if marksheet[0].receipt_URL is not None:
            d=json.loads(marksheet[0].receipt_URL)
            sem=[]
            url=[]
            print(d)
            for i in sorted(d):
                sem.append(i)
                url.append(d[i])
            return render(request,'studentdashboard/receipt.html',{'flag':True,'sem_url':zip(sem, url)})
        else:
            return render(request,'studentdashboard/receipt.html',{'flag':False})

