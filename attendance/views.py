from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Student, Attendance, DeviceLog, Note, Assignment, Submission, UserProfile, Course
from .forms import StudentForm, NoteForm, AssignmentForm, SubmissionForm, GradeForm, CourseForm
import subprocess
import re
from datetime import datetime, timedelta
from django.db.models import Count
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
import os

@login_required
def dashboard(request):
    user_role = request.user.userprofile.role
    context = {'user_role': user_role}

    # Admin Dashboard Data
    if user_role == 'admin':
        total_students = Student.objects.count()
        today_attendance = Attendance.objects.filter(date=timezone.now().date()).count()
        recent_devices = DeviceLog.objects.order_by('-last_seen')[:5]
        
        # Attendance data for the last 7 days
        today = timezone.now().date()
        last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
        attendance_counts = [
            Attendance.objects.filter(date=day).count() for day in last_7_days
        ]
        days_labels = [day.strftime('%a') for day in last_7_days]

        context.update({
            'total_students': total_students,
            'today_attendance': today_attendance,
            'recent_devices': recent_devices,
            'attendance_counts': attendance_counts,
            'days_labels': days_labels,
        })

    # Teacher Dashboard Data
    elif user_role == 'teacher':
        teacher_assignments = Assignment.objects.filter(posted_by=request.user).order_by('-posted_at')[:10]
        context.update({
            'teacher_assignments': teacher_assignments,
        })

    # Student Dashboard Data
    elif user_role == 'student':
        try:
            student_profile = Student.objects.get(email=request.user.email)
            student_attendance = Attendance.objects.filter(student=student_profile).order_by('-date')[:10]
            context.update({
                'student_profile': student_profile,
                'student_attendance': student_attendance,
            })
        except Student.DoesNotExist:
             messages.warning(request, "Your student profile is not linked. Please contact an administrator.")
             # Optionally redirect or show minimal dashboard
             pass

    return render(request, 'attendance/dashboard.html', context)

@login_required
def students(request):
    students = Student.objects.all().order_by('name')
    return render(request, 'attendance/students.html', {'students': students})

@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Student added successfully!')
            return redirect('students')
    else:
        form = StudentForm()
    return render(request, 'attendance/add_student.html', {'form': form})

@login_required
def attendance_log(request):
    date = request.GET.get('date', timezone.now().date())
    attendance = Attendance.objects.filter(date=date).select_related('student')
    return render(request, 'attendance/attendance_log.html', {
        'attendance': attendance,
        'date': date
    })

@login_required
def device_log(request):
    devices = DeviceLog.objects.all().order_by('-last_seen')
    return render(request, 'attendance/device_log.html', {'devices': devices})

@login_required
def scan_devices(request):
    try:
        # Get ARP table using system command
        arp_output = subprocess.check_output("arp -a", shell=True).decode()
        devices = []
        
        # Parse ARP output
        for line in arp_output.split('\n'):
            match = re.search(r'([0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2}[:-][0-9a-fA-F]{2})', line)
            if match:
                mac = match.group(1)
                ip_match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
                ip = ip_match.group(1) if ip_match else "Unknown"
                
                # Check if device is known
                student = Student.objects.filter(mac_address=mac).first()
                
                # Update or create device log
                device_log, created = DeviceLog.objects.get_or_create(
                    mac_address=mac,
                    defaults={
                        'ip_address': ip,
                        'is_known': bool(student),
                        'student': student
                    }
                )
                
                if not created:
                    device_log.ip_address = ip
                    device_log.last_seen = timezone.now()
                    device_log.is_known = bool(student)
                    device_log.student = student
                    device_log.save()
                
                # If device is known and student is present, mark attendance
                if student and not Attendance.objects.filter(
                    student=student,
                    date=timezone.now().date()
                ).exists():
                    Attendance.objects.create(
                        student=student,
                        date=timezone.now().date(),
                        time_in=timezone.now().time(),
                        status='present'
                    )
        
        messages.success(request, 'Device scan completed successfully!')
    except Exception as e:
        messages.error(request, f'Error scanning devices: {str(e)}')
    
    return redirect('dashboard')

@login_required
def notes_list(request):
    notes = Note.objects.all().order_by('-upload_date')
    return render(request, 'attendance/notes_list.html', {'notes': notes})

@login_required
def upload_note(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.uploaded_by = request.user
            note.save()
            messages.success(request, 'Note uploaded successfully!')
            return redirect('notes_list')
    else:
        form = NoteForm()
    return render(request, 'attendance/upload_note.html', {'form': form})

@login_required
def download_note(request, note_id):
    note = Note.objects.get(id=note_id)
    file_path = note.file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
            return response
    raise Http404

@login_required
def assignments_list(request):
    assignments = Assignment.objects.all().order_by('-posted_at')
    return render(request, 'attendance/assignments_list.html', {'assignments': assignments})

@login_required
def assignment_detail(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    submissions = Submission.objects.filter(assignment=assignment)
    user_submission = None
    if request.user.userprofile.role == 'student':
        user_submission = submissions.filter(student=request.user).first()
    return render(request, 'attendance/assignment_detail.html', {
        'assignment': assignment,
        'submissions': submissions,
        'user_submission': user_submission
    })

@login_required
def post_assignment(request):
    if request.user.userprofile.role != 'teacher':
        messages.error(request, 'Only teachers can post assignments.')
        return redirect('assignments_list')
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.posted_by = request.user
            assignment.save()
            messages.success(request, 'Assignment posted successfully!')
            return redirect('assignments_list')
    else:
        form = AssignmentForm()
    return render(request, 'attendance/post_assignment.html', {'form': form})

@login_required
def submit_assignment(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    if request.user.userprofile.role != 'student':
        messages.error(request, 'Only students can submit assignments.')
        return redirect('assignments_list')
    if Submission.objects.filter(assignment=assignment, student=request.user).exists():
        messages.error(request, 'You have already submitted this assignment.')
        return redirect('assignment_detail', assignment_id=assignment.id)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user
            submission.save()
            messages.success(request, 'Assignment submitted successfully!')
            return redirect('assignment_detail', assignment_id=assignment.id)
    else:
        form = SubmissionForm()
    return render(request, 'attendance/submit_assignment.html', {'form': form, 'assignment': assignment})

@login_required
def grade_submission(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    if request.user.userprofile.role != 'teacher':
        messages.error(request, 'Only teachers can grade submissions.')
        return redirect('assignment_detail', assignment_id=submission.assignment.id)
    if request.method == 'POST':
        form = GradeForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, 'Submission graded successfully!')
            return redirect('assignment_detail', assignment_id=submission.assignment.id)
    else:
        form = GradeForm(instance=submission)
    return render(request, 'attendance/grade_submission.html', {'form': form, 'submission': submission})

@login_required
def courses_list(request):
    user_role = request.user.userprofile.role
    if user_role == 'teacher':
        courses = Course.objects.filter(teacher=request.user)
    elif user_role == 'student':
        student = Student.objects.get(email=request.user.email)
        courses = student.courses_enrolled.all()
    else:  # admin
        courses = Course.objects.all()
    return render(request, 'attendance/courses_list.html', {'courses': courses})

@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    assignments = course.assignments.all().order_by('-posted_at')
    students = course.students.all()
    return render(request, 'attendance/course_detail.html', {
        'course': course,
        'assignments': assignments,
        'students': students
    })

@login_required
def add_course(request):
    if request.user.userprofile.role not in ['admin', 'teacher']:
        messages.error(request, 'You do not have permission to add courses.')
        return redirect('courses_list')
        
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save()
            messages.success(request, 'Course added successfully!')
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm()
    return render(request, 'attendance/add_course.html', {'form': form})

@login_required
def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.user.userprofile.role not in ['admin', 'teacher'] or (request.user.userprofile.role == 'teacher' and course.teacher != request.user):
        messages.error(request, 'You do not have permission to edit this course.')
        return redirect('courses_list')
        
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('course_detail', course_id=course.id)
    else:
        form = CourseForm(instance=course)
    return render(request, 'attendance/edit_course.html', {'form': form, 'course': course})
