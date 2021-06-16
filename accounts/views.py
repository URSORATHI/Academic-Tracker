from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import student,subject
#from .forms import subjectform
from django.contrib.auth import authenticate
from django.db import models
from django.http import JsonResponse
import re
from io import TextIOWrapper
from accounts.models import attendance, AdminR, StudentsR, adminsubject
from accounts.resources import attendanceResource
from tablib import Dataset

def changepass(request):
    if request.method == "POST":
        email = request.POST.get('email1')
        password = request.POST.get('password1')
        npass = request.POST.get('newpassword')
        a = AdminR.objects.filter(email1=email,password1=password).values('email1','password1')
        print(a)
        if a:
            b = AdminR.objects.get(email1=email)
            b.password1 = npass
            b.save()
            return redirect("/adminlogin")
        else:
            messages.error(request, 'Invalid Credentials!')
            return redirect("/changepass")
    else:
        return render(request, 'changepass.html')

def stuchangepass(request):
    if request.method == "POST":
        email = request.POST.get('email1')
        password = request.POST.get('password1')
        npass = request.POST.get('newpassword')
        a = StudentsR.objects.filter(email=email,password=password).values('email','password')
        print(a)
        if a:
            b = StudentsR.objects.get(email=email)
            b.password = npass
            b.save()
            return redirect("/login")
        else:
            messages.error(request, 'Invalid Credentials!')
            return redirect("/stuchangepass")
    else:
        return render(request, 'stuchangepass.html')
    
    
def adminlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email1')
        password = request.POST.get('password1')
        user = AdminR.objects.filter(email1=email,password1=password).values('email1','password1')
        user2= AdminR.objects.get(email1=email)
        if user : 
            print("working")
            request.session['email'] = user2.email1
            print("Session Started")
            return redirect('http://127.0.0.1:8000/admina')
        else:
            print("error")
            messages.error(request, 'Invaild credentials')
            return redirect('http://127.0.0.1:8000/adminlogin')
    else:
        return render(request, 'adminregisteration.html')

def adminregister(request):
    if request.method == 'POST':
        name= request.POST.get('name')
        email= request.POST.get('email')
        password= request.POST.get('password')
        def ispresent(str):
             regex = ("^(?=.*[a-z])(?=." +
             "*[A-Z])(?=.*\\d)" +
             "(?=.*[-+_!@#$%^&*., ?]).+$")
             p = re.compile(regex)
             if(re.search(p, str) and len(str) >= 8):
                return True
             else:
                return False
        a = AdminR.objects.filter(email1=email).values('email1')
        if a:
            messages.error(request, 'This email already exists!')
            return redirect('/adminlogin')
        elif ispresent(password):
        #else:
            adminr = AdminR(username1=name, email1=email, password1=password)
            adminr.save()
        else:
            messages.error(request, 'Password error')
        return redirect('http://127.0.0.1:8000/adminregister')
    else:
        return render(request, 'adminregisteration.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email1')
        password = request.POST.get('password1')
        user = StudentsR.objects.filter(email=email,password=password).values('email','password')
        user2= StudentsR.objects.get(email=email)
        if user : 
            print("working")
            request.session['email'] = user2.email
            print("Session Started")
            return redirect('http://127.0.0.1:8000/student')
        else:
            print("error")
            messages.info(request, 'Invaild credentials')
            return redirect('http://127.0.0.1:8000/login')
    else:
        return render(request, 'registeration.html')
   
def register(request):
    if request.method == 'POST':
        name= request.POST.get('name')
        email= request.POST.get('email')
        password= request.POST.get('password')
        def ispresent(str):
             regex = ("^(?=.*[a-z])(?=." +
             "*[A-Z])(?=.*\\d)" +
             "(?=.*[-+_!@#$%^&*., ?]).+$")
             p = re.compile(regex)
             if(re.search(p, str) and len(str) >= 8):
                return True
             else:
                return False
        a = StudentsR.objects.filter(email=email).values('email')
        if a:
            messages.error(request, 'This email already exists!')
            return redirect('http://127.0.0.1:8000/login')
        elif ispresent(password):
        #else:
            studentr = StudentsR(username=name, email=email, password=password)
            studentr.save()
        else:
            messages.error(request, 'Password error')
        return redirect('http://127.0.0.1:8000/login')

    else:
        return render(request, 'registeration.html')

def logout(request):
    del request.session['email']
    print("Session Ended")
    return redirect('http://127.0.0.1:8000/home')
    


def chart(request):
    labels = []
    data = []
    labels1 = []
    data1 = []
    a = []
    s = 0
    r = 0
    user = StudentsR.objects.all()
    # queryset = subject.objects.order_by('-name')[:2]
    queryset = subject.objects.all()
    for sub in queryset:
        if request.session['email']:
            session = request.session.get('email')
            sub_email= sub.email
            if session == sub_email:

                print("User printed")
                if sub.attendance:
                    x = (sub.attendance/sub.total_lectures)*100
                    labels.append(sub.subjectname)
                    data.append(x)
                print(sub.subjectname)
                print(sub.attendance)

    
    # queryset1 = subject.objects.order_by('-name')[:2]
    queryset1 = subject.objects.all()
    for sub in queryset1:
        if request.session['email']:
            session = request.session.get('email')
            sub_email = sub.email
            if session == sub_email:
                if sub.marks:
                    labels1.append(sub.subjectname)
                    data1.append(sub.marks)
                print(sub.subjectname)
                print(sub.marks)
            
                if sub.attendance!=0 and sub.total_lectures!=0:
                    
                    r = (sub.attendance/sub.total_lectures)*100
                    if r < 75:
                        s = sub.subjectname
                        a.append(s)

    return render(request, 'student.html', {
        'labels': labels,
        'data': data,
        'labels1': labels1,
        'data1': data1,
        'users': user,
        'subjects': subject.objects.all(),
        'a':a,
    })
    
    
def home(request):
    return render(request, 'home.html')

def admin(request):
    return render(request, 'admin.html')

def admina(request):
    return render(request, 'admina.html')

# Create your views here.
    
def form(request):
    user=AdminR.objects.all()
    if request.method == 'POST': 
        
        names= [x.username for x in StudentsR.objects.all()]
        student_ids = []
        for x in names:
            if request.POST.get(x):
                student_ids.append(int(request.POST.get(x))) 
                print(x)
                print('hi')

            else:
                print('hello')
                print(x)
        if request.POST.get('subjectname1') and request.POST.get('marks1') and request.POST.get('totalmarks1'):
            subjectname= request.POST.get('subjectname1')
            marks= request.POST.get('marks1')
            totalmarks= request.POST.get('totalmarks1')
            subject1 =subject.objects.create(subjectname = subjectname, marks= marks, total_marks = totalmarks)
        if request.POST.get('subjectname2') and request.POST.get('marks2') and request.POST.get('totalmarks2'):
            subjectname= request.POST.get('subjectname2')
            marks= request.POST.get('marks2')
            totalmarks= request.POST.get('totalmarks2')
            subject2 =subject.objects.create(subjectname = subjectname, marks= marks, total_marks = totalmarks)
        if request.POST.get('subjectname3') and request.POST.get('marks3') and request.POST.get('totalmarks3'):
           subjectname= request.POST.get('subjectname3')
           marks= request.POST.get('marks3')
           totalmarks= request.POST.get('totalmarks3')
           subject3 =subject.objects.create(subjectname = subjectname, marks= marks, total_marks = totalmarks)
        if request.POST.get('subjectname4') and request.POST.get('marks4') and request.POST.get('totalmarks4'):
           subjectname= request.POST.get('subjectname4')
           marks= request.POST.get('marks4')
           totalmarks= request.POST.get('totalmarks4')
           subject4 =subject.objects.create(subjectname = subjectname, marks= marks, total_marks = totalmarks)
        if request.POST.get('subjectname5') and request.POST.get('marks5') and request.POST.get('totalmarks5'):
           subjectname= request.POST.get('subjectname5')
           marks= request.POST.get('marks5')
           totalmarks= request.POST.get('totalmarks5')
           subject5 =subject.objects.create(subjectname = subjectname, marks= marks, total_marks = totalmarks)
        for x in student_ids:
            if request.POST.get('subjectname1') and request.POST.get('marks1') and request.POST.get('totalmarks1'):
                subject1.name.add(StudentsR.objects.get(id=x))
                s=StudentsR.objects.get(id=x)
                subject1.email=s.email
                subject1.save()
            if request.POST.get('subjectname2') and request.POST.get('marks2') and request.POST.get('totalmarks2'):
                subject2.name.add(StudentsR.objects.get(id=x))
                s=StudentsR.objects.get(id=x)
                subject2.email=s.email
                subject2.save()
            if request.POST.get('subjectname3') and request.POST.get('marks3') and request.POST.get('totalmarks3'):
                subject3.name.add(StudentsR.objects.get(id=x))
                s=StudentsR.objects.get(id=x)
                subject3.email=s.email
                subject3.save()
            if request.POST.get('subjectname4') and request.POST.get('marks4') and request.POST.get('totalmarks4'):
                subject4.name.add(StudentsR.objects.get(id=x))
                s=StudentsR.objects.get(id=x)
                subject4.email=s.email
                subject4.save()
            if request.POST.get('subjectname5') and request.POST.get('marks5') and request.POST.get('totalmarks5'):
                subject5.name.add(StudentsR.objects.get(id=x))
                s=StudentsR.objects.get(id=x)
                subject5.email=s.email
                subject5.save()
            print(x)
        print('user_created')
        return redirect('http://127.0.0.1:8000/admina')

    else:
        return render(request, 'admina.html', {"names": StudentsR.objects.all(), "users" : user, "subjects": adminsubject.objects.all(),})
    
    
def simple_upload(request):    
    print(request.POST,request.FILES)
    if request.method == 'POST': 
        print("hola")
        subjectname= request.POST.get('subjectname')
        print(subjectname)
        dataset = Dataset()
        new_attendance = TextIOWrapper(request.FILES['myfile'].file, encoding=request.encoding)
        imported_data = dataset.load(new_attendance.read(),format='csv')
        print(imported_data,"hello")
        for i in imported_data: 
            print(i[0],i[1],"hi")
            value = attendance(name=i[1],population="qwer")
            value.save()
            print(value,value.id)
        queryset = attendance.objects.all()
        queryset1 = subject.objects.all()
       
        
        if request.session['email']:
            session = request.session.get('email')
            if adminsubject.objects.filter(subjectname=subjectname,email=session ).exists():
                sub1=adminsubject.objects.get(subjectname=subjectname)
                e=sub1.total_lectures
                f=int(e)+1
                sub1.total_lectures=f
                print(f,"unnati")
                sub1.save()
            else:
                sub2=adminsubject.objects.create(subjectname=subjectname)
                sub2.total_lectures=1
                sub2.email=session
                sub2.save()
        
                
            
                
        for sub in queryset1:
            if subjectname==sub.subjectname:
                if sub.total_lectures is None:
                    sub.total_lectures =1
                    sub.save()
                else:
                    c=sub.total_lectures
                    d=int(c)+1
                    sub.total_lectures=d
                    sub.save()
                    print(sub.subjectname)
                    for i in queryset:
                        print(i.name)
                        for s in sub.name.all():
                            print(s.username)
                            if s.username==i.name:
                                if sub.attendance is None:
                                    sub.attendance=1
                                    sub.save()
                                else:
                                    a=sub.attendance
                                    b=int(a)+1
                                    sub.attendance=b
                                    sub.save()
                                    print(sub.attendance)
                             
                                    print("2")
                      
    attendance.objects.all().delete()        
    print("hi")     
    return JsonResponse({"message":"Sucess"},status=201)
    return render(request, 'admina.html')    
    


