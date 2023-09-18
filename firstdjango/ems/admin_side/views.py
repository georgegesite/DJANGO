from django.shortcuts import render, redirect
from turtle import pos
from .models import *
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages 

def home(request):
    return render(request, 'index.html')

def admin_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    emp_data = Employee.objects.filter()
    on_leave = emp_data.filter(on_leave=True)
    d = {'total_employee':emp_data.count(), 'on_leave':on_leave.count()}
    return render(request, 'admin_dashboard.html',d)

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
    return render(request, 'emp_login2.html',d)

def registration(request):
    error = ""
    if request.method == "POST":
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        ec = request.POST['empcode']
        em = request.POST['email']
        pwd = request.POST['pwd']
        try:
            user = User.objects.create_user(first_name=fn, last_name=ln, username=em,password=pwd)
            Employee.objects.create(user = user , empcode=ec)
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'registration.html',d)

def emp_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('emp_login')
    return render(request, 'emp_dashboard.html')

def employee_list(request):
    emp_data = Employee.objects.filter()
    d = {'employee':emp_data}
    return render(request, 'employee_list.html',d)

def edit_employee(request, pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    emp_data =Employee.objects.get(id=pid)
    if request.method == "POST":
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        ec = request.POST['empcode']
        dob = request.POST['dob']
        doj = request.POST['doj']
        address = request.POST['address']
        city = request.POST['city']
        region = request.POST['region']
        zipcode = request.POST['zipcode']
        country = request.POST['country']
        department = request.POST['department']
        position = request.POST['position']

        emp_data.user.first_name = fn
        emp_data.user.last_name = ln
        emp_data.empcode = ec
        emp_data.dob = dob
        emp_data.doj = doj
        emp_data.address = address
        emp_data.city = city
        emp_data.region = region
        emp_data.zipcode = zipcode
        emp_data.country = country
        emp_data.department = department
        emp_data.position = position
        
        if doj:
            emp_data.doj = doj
        try:
            emp_data.save()
            emp_data.user.save()
            error = "no"
        except:
            error = "yes"
    d = {'error': error,'emp_data': emp_data}        
    return render(request, 'edit_employeee.html', d)

def delete_employee(request, pid):
    data = Employee.objects.get(id=pid)
    data.delete()
    messages.success(request, "Employee Deleted successfully")
    return redirect('employee_list')

def leave_status(request, pid):
    data = Employee.objects.get(id=pid)
    if data.on_leave:
        data.on_leave = False
    else:
        data.leave_count = data.leave_count + 1
        data.on_leave = True
    data.save()
    messages.success(request, "Employee leave status Changed successfully.")
    return redirect('employee_list')

def Logout(request):
    logout(request)
    return redirect('/')