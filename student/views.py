from django.shortcuts import render,HttpResponse,redirect
from Admin.models import Student,Marksheet,Subjects
from django.contrib import messages

def login(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('adminlogin/addstudent')
        else:
            return redirect('dashboard')
    else:
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

def pointer(request):
    if request.method=='POST':
        flag=int(request.POST.get('flag'))
        if(flag==0):
            sem=int(request.POST.get('semester'))
            branch=request.POST.get('branch')
            subject=Subjects.objects.filter(sem=sem,branch=branch)
            print(subject)
            for i in subject:
                print(i.sub_name)
            return render(request,'studentdashboard/pointer.html',{'subject':subject,'show':False})
        else:
            print(request.POST)
            d=request.POST.copy()
            del d['csrfmiddlewaretoken']
            del d['flag']
            sumobtaincredit=0
            sumtotalcredit=0
            l=[]
            grade={10:'O',9:'A+',8:'A',7:'B+',6:'B',5:'C',4:'P',0:'F'}
            for i in d:
                key=i[:-1]
                print(i[-1])
                print(key)
                s=Subjects.objects.filter(sub_name=key)
                print(s)
                d_r={}
                d_r['sub_name']=key
                for j in s:
                    if(i[-1]=='p'):
                        print('in p')
                        print(int(d[i]),j.practical_credit)
                        sumobtaincredit+=int(d[i])*j.practical_credit
                        sumtotalcredit+=j.practical_credit
                        d_r['practical_credit']=1
                        d_r['grade']=grade[int(d[i])]
                    else:
                        print('in t')
                        print(int(d[i]),j.theory_credit)
                        sumobtaincredit+=int(d[i])*j.theory_credit
                        sumtotalcredit+=j.theory_credit
                        d_r['theory_credit']=1
                        d_r['grade']=grade[int(d[i])]
                l.append(d_r)
            print(sumobtaincredit,sumtotalcredit)
            sgpa=round(sumobtaincredit/sumtotalcredit,2)
            print(sgpa)
            print(l)

            return render(request,'studentdashboard/result.html',{'subject':l,'SGPA':sgpa})
    else:
        '''
        import pandas as pd
        df = pd.read_excel ('G:\LastSemProject\doclocker\student\Example3.xlsx')
        print(df)
        for i in df.itertuples():
            sem=i[1]
            name=i[3]
            branch=i[2]
            theory=i[4]
            practical=i[5]
            student =Subjects.objects.create(sem = sem,sub_name=name,theory_credit=theory,practical_credit=practical,branch=branch)
        '''
        return render(request,'studentdashboard/pointer.html',{'show':True})

def profile(request):
    email=request.user.email
    student=Student.objects.filter(email=email)
    session_end=int(student[0].session)+4    
    return render(request,'studentdashboard/profile.html',{'student':student[0],'end':session_end})