from django import forms
from .models import *


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ["title", "description"]


class DateInput(forms.DateInput):
    input_type = "date"


class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        widgets = {"due_date": DateInput()}
        fields = ["subject", "title", "description", "due_date", "is_finished"]


class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100, label="Enter your Search : ")


class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        widgets = {"created": DateInput()}
        fields = ["title", "is_finished"]
