# board/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Announcement(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.title
    
    def is_expired(self):
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False
    
    class Meta:
        ordering = ['-created_at']

class Event(models.Model):
    EVENT_TYPE_CHOICES = [
        ('lecture', 'Lecture'),
        ('exam', 'Examination'),
        ('meeting', 'Meeting'),
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES, default='other')
    venue = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def is_today(self):
        today = timezone.now().date()
        return self.start_date.date() <= today <= self.end_date.date()
    
    def is_upcoming(self):
        return self.start_date.date() > timezone.now().date()
    
    class Meta:
        ordering = ['start_date']

class Timetable(models.Model):
    DAY_CHOICES = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES)
    course_code = models.CharField(max_length=20)
    course_title = models.CharField(max_length=200)
    lecturer = models.CharField(max_length=100)
    venue = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    level = models.CharField(max_length=20, default='100L')
    semester = models.CharField(max_length=20, default='First')
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.course_code} - {self.day_of_week} {self.start_time}"
    
    class Meta:
        ordering = ['day_of_week', 'start_time']

class Result(models.Model):
    SEMESTER_CHOICES = [
        ('first', 'First Semester'),
        ('second', 'Second Semester'),
    ]
    
    session = models.CharField(max_length=20)  # e.g., "2023/2024"
    semester = models.CharField(max_length=10, choices=SEMESTER_CHOICES)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    level = models.CharField(max_length=20)  # e.g., "200L"
    course_code = models.CharField(max_length=20)
    course_title = models.CharField(max_length=200)
    file_url = models.URLField(blank=True)  # Link to result document
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.course_code} - {self.session} {self.semester}"
    
    class Meta:
        ordering = ['-created_at']