from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="manager@pgfood.com",
            password="ManagerPassword123!",
            full_name="Rajesh Kumar",
            mobile_number="+91 9123456789",
            role=User.Role.MANAGER
        )

    def test_user_properties(self):
        self.assertEqual(self.user.short_name, "Rajesh")
        self.assertEqual(self.user.initials, "RK")
        self.assertEqual(self.user.display_role, "Operations Manager")
        self.assertTrue(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_superuser_creation(self):
        admin = User.objects.create_superuser(
            email="super@pgfood.com",
            password="SuperPassword123!",
            full_name="Super Admin"
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertEqual(admin.role, User.Role.SUPERADMIN)


class AuthenticationViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            email="testadmin@pgfood.com",
            password="StrongPassword123!",
            full_name="Test Administrator",
            mobile_number="+91 9876543210"
        )

    def test_login_page_renders(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign in to your food delivery administrator account")
        self.assertContains(response, "Remember me on this device")

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse("accounts:login"), {
            "email": "testadmin@pgfood.com",
            "password": "WrongPassword!",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid email address or password")

    def test_login_successful_redirect(self):
        response = self.client.post(reverse("accounts:login"), {
            "email": "testadmin@pgfood.com",
            "password": "StrongPassword123!",
            "remember_me": True
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("dashboard:index"))

    def test_logout(self):
        self.client.login(email="testadmin@pgfood.com", password="StrongPassword123!")
        response = self.client.post(reverse("accounts:logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("accounts:login"))


class ProfileAndSecurityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = User.objects.create_superuser(
            email="profileadmin@pgfood.com",
            password="CurrentPassword123!",
            full_name="Profile Admin",
            mobile_number="+91 9000000000"
        )
        self.client.login(email="profileadmin@pgfood.com", password="CurrentPassword123!")

    def test_profile_page_loads(self):
        response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Profile Details")
        self.assertContains(response, "Profile Admin")

    def test_profile_update(self):
        response = self.client.post(reverse("accounts:profile"), {
            "full_name": "Updated Admin Name",
            "email": "profileadmin@pgfood.com",
            "mobile_number": "+91 9999999999"
        })
        self.assertEqual(response.status_code, 302)
        self.admin.refresh_from_db()
        self.assertEqual(self.admin.full_name, "Updated Admin Name")
        self.assertEqual(self.admin.mobile_number, "+91 9999999999")

    def test_password_change_success(self):
        response = self.client.post(reverse("accounts:change_password"), {
            "current_password": "CurrentPassword123!",
            "new_password": "NewStrongPassword456!",
            "confirm_new_password": "NewStrongPassword456!"
        })
        self.assertEqual(response.status_code, 302)
        self.admin.refresh_from_db()
        self.assertTrue(self.admin.check_password("NewStrongPassword456!"))

    def test_password_change_wrong_current(self):
        response = self.client.post(reverse("accounts:change_password"), {
            "current_password": "IncorrectPassword123!",
            "new_password": "NewStrongPassword456!",
            "confirm_new_password": "NewStrongPassword456!"
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The current password entered is incorrect.")
