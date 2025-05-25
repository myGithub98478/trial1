from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('students/', views.students, name='students'),
    path('students/add/', views.add_student, name='add_student'),
    path('attendance/', views.attendance_log, name='attendance_log'),
    path('devices/', views.device_log, name='device_log'),
    path('scan/', views.scan_devices, name='scan_devices'),
    path('notes/', views.notes_list, name='notes_list'),
    path('notes/upload/', views.upload_note, name='upload_note'),
    path('notes/download/<int:note_id>/', views.download_note, name='download_note'),
    path('assignments/', views.assignments_list, name='assignments_list'),
    path('assignments/post/', views.post_assignment, name='post_assignment'),
    path('assignments/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    path('assignments/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
    path('submissions/<int:submission_id>/grade/', views.grade_submission, name='grade_submission'),
    path('courses/', views.courses_list, name='courses_list'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/edit/', views.edit_course, name='edit_course'),
] 