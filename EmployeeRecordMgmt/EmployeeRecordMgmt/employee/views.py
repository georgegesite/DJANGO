from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import login,logout,authenticate
from datetime import date
# Create your views here.

def index(request):
    return render(request, 'index.html')

def registration(request):
    error = ""
    if request.method == "POST":
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        ec = request.POST['empcode']
        em = request.POST['email']
        pwd = request.POST['pwd']
        try:
            user = User.objects.create_user(first_name=fn, last_name=ln,username=em,password=pwd)
            EmployeeDetail.objects.create(user = user , empcode=ec)
            EmployeeExperience.objects.create(user=user)
            EmployeeEducation.objects.create(user=user)
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'registration.html',d)

def emp_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['emailid']
        p = request.POST['password']
        user = authenticate(username=u,password=p)
        if user:
            login(request, user)
            error = "no"
        else:
            error = "yes"
    d = {'error': error}
    return render(request, 'emp_login.html',d)

def Logout(request):
    logout(request)
    return redirect('/')

def emp_home(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    return render(request, 'emp_home.html')

def profile(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    error = ""
    user = request.user
    employee = EmployeeDetail.objects.get(user=user)
    if request.method == "POST":
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        ec = request.POST['empcode']
        dept = request.POST['department']
        designation = request.POST['designation']
        contact = request.POST['contact']
        jdate = request.POST['jdate']
        gender = request.POST['gender']

        employee.user.first_name = fn
        employee.user.last_name = ln
        employee.empcode = ec
        employee.empdept = dept
        employee.designation = designation
        employee.contact = contact
        employee.gender = gender

        if jdate:
            employee.joiningdate = jdate
        try:
            employee.save()
            employee.user.save()
            error = "no"
        except:
            error = "yes"
    d = {'error': error,'employee': employee}
    return render(request, 'profile.html',d)


def myexperience(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')

    user = request.user
    experience = EmployeeExperience.objects.get(user=user)


    d = {'experience': experience}
    return render(request, 'myexperience.html',d)

def edit_myexperience(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')

    user = request.user
    experience = EmployeeExperience.objects.get(user=user)

    if request.method == "POST":
        cn1 = request.POST['company1name']
        cdes1 = request.POST['company1desig']
        csal1 = request.POST['company1salary']
        cd1 = request.POST['company1duration']

        cn2 = request.POST['company2name']
        cdes2 = request.POST['company2desig']
        csal2 = request.POST['company2salary']
        cd2 = request.POST['company2duration']

        cn3 = request.POST['company3name']
        cdes3 = request.POST['company3desig']
        csal3 = request.POST['company3salary']
        cd3 = request.POST['company3duration']

        experience.company1name = cn1
        experience.company1desig = cdes1
        experience.company1salary = csal1
        experience.company1duration = cd1

        experience.company2name = cn2
        experience.company2desig = cdes2
        experience.company2salary = csal2
        experience.company2duration = cd2

        experience.company3name = cn3
        experience.company3desig = cdes3
        experience.company3salary = csal3
        experience.company3duration = cd3

        try:
            experience.save()
            error = "no"
        except:
            error = "yes"

    return render(request, 'edit_myexperience.html',locals())


def myeducation(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')

    user = request.user
    education = EmployeeEducation.objects.get(user=user)


    d = {'education': education}
    return render(request, 'myeducation.html',d)

def edit_myeducation(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')

    user = request.user
    education = EmployeeEducation.objects.get(user=user)

    if request.method == "POST":
        cpg = request.POST['coursepg']
        scpg = request.POST['schoolclgpg']
        ypg = request.POST['yearpassingpg']
        ppg = request.POST['percentagepg']

        cg = request.POST['coursegra']
        scg = request.POST['schoolclggra']
        yg = request.POST['yearpassinggra']
        pg = request.POST['percentagegra']

        cssc = request.POST['coursessc']
        scssc = request.POST['schoolclgssc']
        ypssc = request.POST['yearpassingssc']
        pssc = request.POST['percentagessc']

        chsc = request.POST['coursehsc']
        schsc = request.POST['schoolclghsc']
        yhsc = request.POST['yearpassinghsc']
        phsc = request.POST['percentagehsc']


        education.coursepg = cpg
        education.schoolclgpg = scpg
        education.yearpassingpg = ypg
        education.percentagepg = ppg

        education.coursegra = cg
        education.schoolclggra = scg
        education.yearpassinggra = yg
        education.percentagegra = pg

        education.coursessc = cssc
        education.schoolclgssc = scssc
        education.yearpassingssc = ypssc
        education.percentagessc = pssc

        education.coursehsc = chsc
        education.schoolclghsc = schsc
        education.yearpassinghsc = yhsc
        education.percentagehsc = phsc

        try:
            education.save()
            error = "no"
        except:
            error = "yes"

    return render(request, 'edit_myeducation.html',locals())


def change_password(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    error = ""
    if request.method=="POST":
        o = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"

    return render(request,'change_password.html',locals())


def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    return render(request, 'admin_login.html',locals())


def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    return render(request, 'admin_home.html')


def change_passwordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    if request.method=="POST":
        o = request.POST['currentpassword']
        n = request.POST['newpassword']
        try:
            u = User.objects.get(id=request.user.id)
            if u.check_password(o):
                u.set_password(n)
                u.save()
                error = "no"
            else:
                error = "not"
        except:
            error = "yes"

    return render(request,'change_passwordadmin.html',locals())

def all_employee(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    employee = EmployeeDetail.objects.all()
    return render(request, 'all_employee.html',locals())

def delete_employee(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('all_employee')


def edit_profile(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    employee = EmployeeDetail.objects.get(id=pid)
    if request.method == "POST":
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        ec = request.POST['empcode']
        dept = request.POST['department']
        designation = request.POST['designation']
        contact = request.POST['contact']
        jdate = request.POST['jdate']
        gender = request.POST['gender']

        employee.user.first_name = fn
        employee.user.last_name = ln
        employee.empcode = ec
        employee.empdept = dept
        employee.designation = designation
        employee.contact = contact
        employee.gender = gender

        if jdate:
            employee.joiningdate = jdate
        try:
            employee.save()
            employee.user.save()
            error = "no"
        except:
            error = "yes"
    d = {'error': error,'employee': employee}
    return render(request, 'edit_profile.html',d)


def edit_education(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    user = User.objects.get(id=pid)
    education = EmployeeEducation.objects.get(user=user)

    if request.method == "POST":
        cpg = request.POST['coursepg']
        scpg = request.POST['schoolclgpg']
        ypg = request.POST['yearpassingpg']
        ppg = request.POST['percentagepg']

        cg = request.POST['coursegra']
        scg = request.POST['schoolclggra']
        yg = request.POST['yearpassinggra']
        pg = request.POST['percentagegra']

        cssc = request.POST['coursessc']
        scssc = request.POST['schoolclgssc']
        ypssc = request.POST['yearpassingssc']
        pssc = request.POST['percentagessc']

        chsc = request.POST['coursehsc']
        schsc = request.POST['schoolclghsc']
        yhsc = request.POST['yearpassinghsc']
        phsc = request.POST['percentagehsc']


        education.coursepg = cpg
        education.schoolclgpg = scpg
        education.yearpassingpg = ypg
        education.percentagepg = ppg

        education.coursegra = cg
        education.schoolclggra = scg
        education.yearpassinggra = yg
        education.percentagegra = pg

        education.coursessc = cssc
        education.schoolclgssc = scssc
        education.yearpassingssc = ypssc
        education.percentagessc = pssc

        education.coursehsc = chsc
        education.schoolclghsc = schsc
        education.yearpassinghsc = yhsc
        education.percentagehsc = phsc

        try:
            education.save()
            error = "no"
        except:
            error = "yes"

    return render(request, 'edit_education.html',locals())


def edit_experience(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')

    user = User.objects.get(id=pid)
    experience = EmployeeExperience.objects.get(user=user)

    if request.method == "POST":
        cn1 = request.POST['company1name']
        cdes1 = request.POST['company1desig']
        csal1 = request.POST['company1salary']
        cd1 = request.POST['company1duration']

        cn2 = request.POST['company2name']
        cdes2 = request.POST['company2desig']
        csal2 = request.POST['company2salary']
        cd2 = request.POST['company2duration']

        cn3 = request.POST['company3name']
        cdes3 = request.POST['company3desig']
        csal3 = request.POST['company3salary']
        cd3 = request.POST['company3duration']

        experience.company1name = cn1
        experience.company1desig = cdes1
        experience.company1salary = csal1
        experience.company1duration = cd1

        experience.company2name = cn2
        experience.company2desig = cdes2
        experience.company2salary = csal2
        experience.company2duration = cd2

        experience.company3name = cn3
        experience.company3desig = cdes3
        experience.company3salary = csal3
        experience.company3duration = cd3

        try:
            experience.save()
            error = "no"
        except:
            error = "yes"

    return render(request, 'edit_experience.html',locals())


