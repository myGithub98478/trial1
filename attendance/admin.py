from django.contrib import admin
from .models import Student, Attendance, DeviceLog, UserProfile, Note, Assignment, Submission

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'name', 'mac_address', 'email', 'created_at')
    search_fields = ('student_id', 'name', 'mac_address', 'email')
    list_filter = ('created_at',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'time_in', 'time_out', 'status')
    list_filter = ('date', 'status')
    search_fields = ('student__name', 'student__student_id')

@admin.register(DeviceLog)
class DeviceLogAdmin(admin.ModelAdmin):
    list_display = ('mac_address', 'ip_address', 'first_seen', 'last_seen', 'is_known', 'student')
    list_filter = ('is_known', 'first_seen', 'last_seen')
    search_fields = ('mac_address', 'ip_address', 'student__name')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'upload_date')
    search_fields = ('title', 'uploaded_by__username')
    list_filter = ('upload_date',)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_by', 'deadline', 'posted_at')
    search_fields = ('title', 'posted_by__username')
    list_filter = ('deadline', 'posted_at')

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at', 'marks')
    search_fields = ('assignment__title', 'student__username')
    list_filter = ('submitted_at',)
