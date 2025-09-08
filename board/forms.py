# board/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Announcement, Event, Timetable, Result, Department

class AdminLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Username',
            'required': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Password',
            'required': True
        })
    )

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'department', 'priority', 'expires_at']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter announcement title'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Enter announcement content',
                'rows': 5
            }),
            'department': forms.Select(attrs={
                'class': 'form-select'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'expires_at': forms.DateTimeInput(attrs={
                'class': 'form-input',
                'type': 'datetime-local'
            })
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'department', 'event_type', 'venue', 'start_date', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter event title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Enter event description',
                'rows': 4
            }),
            'department': forms.Select(attrs={
                'class': 'form-select'
            }),
            'event_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'venue': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter venue'
            }),
            'start_date': forms.DateTimeInput(attrs={
                'class': 'form-input',
                'type': 'datetime-local'
            }),
            'end_date': forms.DateTimeInput(attrs={
                'class': 'form-input',
                'type': 'datetime-local'
            })
        }

class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['department', 'day_of_week', 'course_code', 'course_title', 'lecturer', 
                 'venue', 'start_time', 'end_time', 'level', 'semester']
        widgets = {
            'department': forms.Select(attrs={
                'class': 'form-select'
            }),
            'day_of_week': forms.Select(attrs={
                'class': 'form-select'
            }),
            'course_code': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., CIT306'
            }),
            'course_title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Web Design and Programming'
            }),
            'lecturer': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Lecturer name'
            }),
            'venue': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., ICT Hall 1'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-input',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-input',
                'type': 'time'
            }),
            'level': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., 300L'
            }),
            'semester': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., First'
            })
        }

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['session', 'semester', 'department', 'level', 'course_code', 
                 'course_title', 'file_url', 'description']
        widgets = {
            'session': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., 2023/2024'
            }),
            'semester': forms.Select(attrs={
                'class': 'form-select'
            }),
            'department': forms.Select(attrs={
                'class': 'form-select'
            }),
            'level': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., 300L'
            }),
            'course_code': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., CIT306'
            }),
            'course_title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Course title'
            }),
            'file_url': forms.URLInput(attrs={
                'class': 'form-input',
                'placeholder': 'Link to result document'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Additional information about the result',
                'rows': 3
            })
        }

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name', 'code', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Computer Science'
            }),
            'code': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., CSC'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Department description',
                'rows': 3
            })
        }