from django.db import models
from admin_side.models import User

# Create your models here.
class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)
    reason = models.TextField(blank=True)
    
class Salary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    base_salary = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    working_days = models.IntegerField(default=0)
    withdrawn = models.BooleanField(default=False)