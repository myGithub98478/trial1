from django import forms
from .models import Student, Note, Assignment, Submission, Course

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_id', 'name', 'mac_address', 'email']
        widgets = {
            'mac_address': forms.TextInput(attrs={'placeholder': 'XX-XX-XX-XX-XX-XX'}),
            'email': forms.EmailInput(attrs={'placeholder': 'student@example.com'}),
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'description', 'file']

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'file', 'deadline']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file']

class GradeForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['marks', 'feedback']

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'name', 'description', 'teacher', 'students']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'students': forms.SelectMultiple(attrs={'class': 'select2'})
        } 