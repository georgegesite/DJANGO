"""ems URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 
from admin_side.views import *
from other_features.views import *
from other_features.views import UserSalaryView, AdminSalaryView, UpdateBaseSalaryView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('employee-list', employee_list, name="employee_list"),
    path('employee-edit/<int:pid>', edit_employee, name="edit_employee"),
    path('delete_employee/<int:pid>', delete_employee, name="delete_employee"),
    path('leave-status/<int:pid>', leave_status, name="leave_status"),
    path('admin_login',admin_login,name='admin_login'),
    path('admin_dashboard',admin_dashboard,name='admin_dashboard'),
    path('logout/',Logout),
    path('registration/',registration,),
    path('emp_login/',emp_login),
    path('emp_dashboard',emp_dashboard,name='emp_dashboard'),
    path('emp_profile/',profile, ),
    path('change_password',change_password,name='change_password'),
    path('user-attendance/',user_attendance, name='user_attendance'),
    path('admin-attendance/', admin_attendance, name='admin_attendance'),
    path('compensation_request/', compensation_request, name='compensation_request'),
    path('decline_compensation/<int:pk>/', decline_compensation, name='decline_compensation'),
    path('approve_compensation/<int:pk>/', approve_compensation, name='approve_compensation'),
    path('update_attendance/', update_attendance, name='update_attendance'),
    path('user_salary/', UserSalaryView.as_view(), name='user_salary'),
    path('admin_salary/', AdminSalaryView.as_view(), name='admin_salary'),
    path('update_base_salary/<int:pk>', UpdateBaseSalaryView.as_view(), name='update_base_salary'),

]
