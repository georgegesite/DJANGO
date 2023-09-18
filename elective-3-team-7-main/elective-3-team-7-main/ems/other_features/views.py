from django.shortcuts import render,redirect,  get_object_or_404
from django.views import View
from .models import Attendance, Salary
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import UpdateSalaryForm
from django import forms
from django.contrib import messages

# Create your views here.

def user_attendance(request):
    # Get the attendance records for the current user
    attendance_records = Attendance.objects.filter(user=request.user)

    # Check if the form has been submitted
    if request.method == 'POST':
        # Get the form data
        date = request.POST['date']
        present = request.POST['present']
        # Update the attendance record
        # update_attendance(date, present, request)  # remove this line

    context = {'attendance_records': attendance_records}
    # Render the template with the attendance records
    return render(request, 'user_attendance.html', context)

def update_attendance(request):
    if request.method == 'POST':
        date = request.POST['date']
        date_exist = Attendance.objects.filter(date=date).exists()
        if date_exist:
            present = request.POST.get('present', False) == 'True'  # False if not provided
            reason = request.POST['reason']
            # Update the attendance record for the selected date
            attendance, created = Attendance.objects.get_or_create(
                user=request.user, date=date
            )
            attendance.present = present
            attendance.reason = reason
            attendance.save()
        else:
            messages.error(request, 'This date is not in the database')

    return redirect('user_attendance')


    
def compensation_request(request):
    # Check if the form has been submitted
    if request.method == 'POST':
        # Get the date and reason from the form
        date = request.POST['date']
        reason = request.POST['reason']

        # Try to get the attendance record for the given date and user
        try:
            attendance = Attendance.objects.get(date=date, user=request.user)
        except Attendance.DoesNotExist:
            # Return an error if the attendance record does not exist
            hello = {'error': 'Attendance record does not exist'}
            return render(request, 'user_attendance.html', hello )

        # Update the attendance record with the reason
        attendance.reason = reason
        attendance.save()

        # Redirect to the user_attendance view
        return redirect('user_attendance')

def admin_attendance(request):
    # Get the attendance records for all users
    attendance_records = Attendance.objects.all()

    # Get the current URL
    current_url = request.get_full_path()

    # Render the template with the attendance records and current URL
    text = {'attendance_records': attendance_records, 'current_url': current_url}
    return render(request, 'admin_attendance.html', text)

def approve_compensation(request, pk):
    # Get the attendance record with the given primary key
    attendance_record = Attendance.objects.get(pk=pk)

    # Update the attendance record
    attendance_record.present = True
    attendance_record.save()

    # Redirect to the admin dashboard
    return redirect('admin_attendance')

def decline_compensation(request, pk):
    # Get the attendance record with the given primary key
    attendance_record = Attendance.objects.get(pk=pk)

    # Update the attendance record
    attendance_record.present = False
    attendance_record.save()

    # Redirect to the admin dashboard
    return redirect('admin_attendance')

class UserSalaryView(UserPassesTestMixin,View):
    login_url = '/login/'
    raise_exception = True
    def test_func(self):
        return self.request.user.is_authenticated
    def get(self, request):
        try:
            salary = Salary.objects.get(user=request.user)
        except Salary.DoesNotExist:
           salary = Salary.objects.create(user=request.user)
        salary.working_days = Attendance.objects.filter(user=request.user, present=True).count()
        current_salary = salary.base_salary * salary.working_days
        context = {'current_salary': current_salary}
        return render(request, 'user_salary.html', context)
    def post(self, request):
        salary = Salary.objects.get(user=request.user)
        salary.withdrawn = True
        salary.working_days = 0
        salary.save()
        message = "The admin has been notified that you have withdrawn your salary"
        context = {'current_salary': salary.base_salary * salary.working_days, 'message': message}
        return render(request, 'user_salary.html', context)

class AdminSalaryView(UserPassesTestMixin,View):
    login_url = '/login/'
    raise_exception = True
    def test_func(self):
        return self.request.user.is_staff
    def get(self, request):
        salaries = Salary.objects.all()
        for salary in salaries:
            salary.working_days = Attendance.objects.filter(user=salary.user, present=True).count()
            salary.current_salary = salary.base_salary * salary.working_days
        context = {'salaries': salaries}
        return render(request, 'admin_salary.html', context)
    def post(self, request):
        salary_id = request.POST.get('salary_id')
        try:
            salary = Salary.objects.get(id=salary_id)
            salary.base_salary = 0
            Attendance.objects.filter(user=salary.user).delete()
            salary.working_days = 0
            salary.withdrawn = False
            salary.save()
            messages.success(request, f'Attendance records of user {salary.user} were deleted successfully.')
        except Salary.DoesNotExist:
            pass
        return redirect('admin_salary')
        
class UpdateBaseSalaryView(UserPassesTestMixin,View):
    login_url = '/login/'
    raise_exception = True
    def test_func(self):
        return self.request.user.is_staff
    def get(self, request, pk):
        salary = get_object_or_404(Salary, pk=pk)
        form = UpdateSalaryForm(instance=salary)
        context = {'form': form, 'salary': salary}
        return render(request, 'update_base_salary.html', context)
    def post(self, request, pk):
        salary = get_object_or_404(Salary, pk=pk)
        form = UpdateSalaryForm(request.POST, instance=salary)
        if form.is_valid():
            form.save()
        return redirect('admin_salary')

