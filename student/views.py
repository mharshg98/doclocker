from django.shortcuts import render,HttpResponse


def login(request):
    return render(request,'studentlogin.html')
# Create your views here.

def redirect(request):
    return HttpResponse("login succesfull")

