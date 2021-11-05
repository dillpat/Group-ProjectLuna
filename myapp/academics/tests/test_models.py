from django.test import TestCase
from academics.models import Department, Course, Module, StudentModuleEnrolment, ModulePosts, ModuleComment
from users.models import StaffProfile, StudentProfile
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# department test
class DepartmentTest(TestCase):
    # setup for the test, department name
    def setUp(self):
        self.dep_name = Department.objects.create(name="AI")

    # test assert
    def test_department(self):
        """Department is correctly identified"""
        self.assertEqual(self.dep_name.name, "AI")


# Course test
class CourseTest(TestCase):
    # setup for the test, course objcet is created
    def setUp(self):
        Course.objects.create(
            name="Maths and computer science",
            description="Maths course",
            department=Department.objects.create(name="AI"),
        )

    # test assert
    def test_course(self):
        """Course is correctly identified"""
        course = Course.objects.get(id=1)
        self.assertEqual(course.name, "Maths and computer science")
        self.assertEqual(course.description, "Maths course")
        self.assertEqual(course.department.name, "AI")


# Module test
class ModuleTest(TestCase):
    # setup for the test, module objcet is created
    def setUp(self):
        Module.objects.create(
            name="differential equations",
            description="differential equations course",
            course=Course.objects.create(
                name="Maths and computer science",
                description="Maths course",
                department=Department.objects.create(name="AI"),
            ),
            staff=StaffProfile.objects.create(
                user=User.objects.create(), first_login=False
            ),
            goals=["t1", "t2", "t3"],
            planet_representation="planetE",
        )

    # test assert
    def test_module(self):
        """Module is correctly identified"""
        module = Module.objects.get(name="differential equations")
        self.assertEqual(module.name, "differential equations")
        self.assertEqual(module.description, "differential equations course")
        self.assertEqual(module.course.name, "Maths and computer science")
        self.assertEqual(module.staff.first_login, False)
        self.assertEqual(module.goals, ["t1", "t2", "t3"])
        self.assertEqual(module.planet_representation, "planetE")


#
# test for student enrolment
class StudentModuleEnrolmentTest(TestCase):
    # setup for the test, student enrolment object is created
    def setUp(self):
        StudentModuleEnrolment.objects.create(
            module=Module.objects.create(
                name="differential equations",
                description="differential equations course",
                course=Course.objects.create(
                    name="Maths and computer science",
                    description="Maths course",
                    department=Department.objects.create(name="AI"),
                ),
                staff=StaffProfile.objects.create(
                    user=User.objects.create(), first_login=False
                ),
                goals=["t1", "t2", "t3"],
                planet_representation="planetE",
            ),
            student=StudentProfile.objects.create(
                user=User.objects.create(username="person1", password="Luna1234"),
                student_number=1234567890,
                user_rank="Rookie",
                rank_badge="assets/rank1.svg",
                astro_credits=0,
                daily_tasks=[],
                weekly_credits=0,
                weekly_reset_date="2021-03-01",
                daily_reset_date="2021-03-01",
                favourite_module_name="AI",
                personal_goals=[],
                first_login=False,
            ),
            enrolment_date="2021-3-1",
            enrolment_completion_date="2021-3-5",
        )

    # test assert
    def test_ModuleEnrolment(self):
        """Student module enrole is correctly identified"""
        sme = StudentModuleEnrolment.objects.get(id=1)
        self.assertEqual(sme.module.name, "differential equations")
        self.assertEqual(sme.student.student_number, 1234567890)
        self.assertEqual(sme.enrolment_date, datetime.date(2021, 3, 1))
        self.assertEqual(sme.enrolment_completion_date, datetime.date(2021, 3, 5))


# test for Module post, module post object is created
class ModulePostsTest(TestCase):
    @classmethod
    def setUp(self):
        ModulePosts.objects.create(
            title="Post1",
            content="Test post",
            date_posted="2021-3-1",
            author=User.objects.create(username="person2", password="Luna1234"),
            module=Module.objects.create(
                name="differential equations",
                description="differential equations course",
                course=Course.objects.create(
                    name="Maths and computer science",
                    description="Maths course",
                    department=Department.objects.create(name="AI"),
                ),
                staff=StaffProfile.objects.create(
                    user=User.objects.create(), first_login=False
                ),
                goals=["t1", "t2", "t3"],
                planet_representation="planetE",
            ),
        )

    # test assert
    def test_module_post(self):
        post = ModulePosts.objects.get(title = "Post1")
        expected_title = post.title
        expected_content = post.content
        expected_date = post.date_posted.date()
        expected_author = post.author
        expected_module = post.module
        self.assertEqual(expected_title, "Post1")
        self.assertEqual(expected_content, "Test post")
        self.assertEqual(expected_date, datetime.date(2021, 3, 1))
        self.assertEqual(expected_author.username, "person2")
        self.assertEqual(expected_module.name, "differential equations")


class ModuleCommentTest(TestCase):
    @classmethod
    def setUp(self):
        ModuleComment.objects.create(
        post = ModulePosts.objects.create(
            title = "Post2",
            content = "Test post",
            date_posted = "2021-3-1",
            author = User.objects.create(username="person2",
                                     password="Luna1234"),
            module = Module.objects.create(name="differential equations",
                                       description="differential equations course",
                                       course=Course.objects.create(name="Maths and computer science",
                                                                    description="Maths course",
                                                                    department= Department.objects.create(name="AI")),
                                       staff=StaffProfile.objects.create(user=User.objects.create(),
                                                                         first_login=False),
                                       goals = ["t1","t2", "t3"],
                                       planet_representation="planetE")),



        content = "text",
        date_posted = "2021-03-1",
        author =   User.objects.create(username="LunaLover",
                                         password="Luna1234"))

    def test_module_comment(self):
        comment = ModuleComment.objects.get()
        self.assertEqual(comment.post.title, "Post2")
