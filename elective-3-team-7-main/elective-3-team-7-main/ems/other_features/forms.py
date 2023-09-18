from django import forms
from .models import Salary

class UpdateSalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ['base_salary']