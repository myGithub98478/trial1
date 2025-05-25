from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import random
from django.core.management.base import BaseCommand

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    mac_address = models.CharField(max_length=17, unique=True)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.student_id})"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    time_in = models.TimeField(default=timezone.now)
    time_out = models.TimeField(null=True, blank=True)
    status = models.CharField(max_length=20, default='present')  # present, late, absent
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.name} - {self.date}"

class DeviceLog(models.Model):
    mac_address = models.CharField(max_length=17)
    ip_address = models.CharField(max_length=15)
    first_seen = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)
    is_known = models.BooleanField(default=False)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.mac_address} - {self.ip_address}"

class Note(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='notes/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='courses_teaching')
    students = models.ManyToManyField('Student', related_name='courses_enrolled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='assignments/', blank=True, null=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments_posted')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='assignments', null=True, blank=True)
    deadline = models.DateTimeField()
    posted_at = models.DateTimeField(auto_now_add=True)
    total_marks = models.FloatField(default=100)
    is_published = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.course.code if self.course else 'No Course'} - {self.title}"

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    marks = models.FloatField(blank=True, null=True)
    feedback = models.TextField(blank=True)

    def __str__(self):
        return f"{self.assignment.title} - {self.student.username}"
