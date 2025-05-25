from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from attendance.models import Student

# Create your tests here.

class StudentModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            student_id='12345',
            name='Test Student',
            mac_address='00-00-00-00-00-01',
            email='test@student.com'
        )

    def test_student_str(self):
        self.assertEqual(str(self.student), 'Test Student (12345)')

class AuthIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_login(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 302)  # Redirect after login

    def test_logout(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout

class BasicViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser2', password='testpass2')
        self.client.login(username='testuser2', password='testpass2')

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_students_view(self):
        response = self.client.get(reverse('students'))
        self.assertEqual(response.status_code, 200)

    def test_attendance_log_view(self):
        response = self.client.get(reverse('attendance_log'))
        self.assertEqual(response.status_code, 200)

    def test_notes_list_view(self):
        response = self.client.get(reverse('notes_list'))
        self.assertEqual(response.status_code, 200)

    def test_assignments_list_view(self):
        response = self.client.get(reverse('assignments_list'))
        self.assertEqual(response.status_code, 200)
