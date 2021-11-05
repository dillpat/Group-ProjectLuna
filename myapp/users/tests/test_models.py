from django.test import TestCase
from academics.models import (
    Department,
    Course,
    Module,
    StudentModuleEnrolment,
    ModulePosts,
)
from networks.models import NetworkPosts
from users.models import StaffProfile, StudentProfile
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# test for student profile, profile object is created
class StudentProfileTest(TestCase):
    def setUp(self):
        StudentProfile.objects.create(
            user=User.objects.create(username="person3", password="Luna1234"),
            student_number=1234567891,
            user_rank="Rookie",
            rank_badge="assets/rank1.svg",
            astro_credits=10,
            daily_tasks=["t1", "t2", "t3"],
            weekly_credits=5,
            weekly_reset_date="2021-03-01",
            daily_reset_date="2021-03-01",
            favourite_module_name="n/a",
            personal_goals=["t1", "t2", "t3"],
            first_login=False,
        )

    # test assert
    def test_student_profile(self):
        """ Profile correctly selected """
        profile = StudentProfile.objects.get()
        self.assertEqual(profile.user.username, "person3")
        self.assertEqual(profile.student_number, 1234567891)
        self.assertEqual(profile.first_login, False)


# test for staff profile, profile object is created
class StaffProfileTest(TestCase):
    def setUp(self):
        StaffProfile.objects.create(
            user=User.objects.create(username="staff1", password="Luna1234"),
            first_login=False,
        )

    # test assert
    def test_staff_profile(self):
        profile = StaffProfile.objects.get()
        self.assertEqual(profile.user.username, "staff1")
        self.assertEqual(profile.first_login, False)
