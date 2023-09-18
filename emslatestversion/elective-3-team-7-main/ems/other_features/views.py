from django.shortcuts import render,redirect
from .models import Attendance
# Create your views here.

def user_attendance(request):
    # Get the attendance records for the current user
    attendance_records = Attendance.objects.filter(user=request.user)

    # Check if the form has been submitted
    if request.method == 'POST':
        # Get the form data
        date = request.POST['date']
        reason = request.POST['reason']
        # Update the attendance record
        attendance = Attendance.objects.get(user=request.user, date=date)
        attendance.reason = reason
        attendance.save()
        # Redirect to the user_attendance view
        return redirect('user_attendance')
    context = {'attendance_records': attendance_records}
    # Render the template with the attendance records
    return render(request, 'user_attendance.html', context )

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

