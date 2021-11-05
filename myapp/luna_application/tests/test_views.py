from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import views as auth_user
from django.contrib.auth.models import User
from users.models import StudentProfile, StaffProfile
from datetime import datetime, timedelta
from luna_application.views import *
from academics.models import Department, Course, Module, StudentModuleEnrolment, ModulePosts, ModuleComment
from networks.models import NetworkPosts, NetworkComment
import requests
import json


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.start_url = reverse("luna_application-start_page")
        self.login_url = reverse("login")
        self.guest_url = reverse("luna_application-the_hub")
        self.home_url = reverse("luna_application-home_page")
        self.temp_user = User.objects.create(
            username="testUser",
            password="test1234",
        )
        self.temp_profile = StudentProfile.objects.create(
            user=self.temp_user,
            student_number=690923187,
            user_rank="Rookie",
            astro_credits=400,
            weekly_credits=200,
            weekly_reset_date=datetime.now(),
            daily_reset_date=datetime.now(),
            favourite_module_name="Mathematical Modelling",
            first_login=False,
            personal_goals=["Run for 10 minutes", "Learn to cook salad"],
        )
        self.wellbeing_url = reverse("luna_application-wellbeing_tasks")
        self.staff_user = User.objects.create(
            username="testStaff", password="Testing1234"
        )
        self.staff_profile = StaffProfile.objects.create(
            user=self.staff_user,
            first_login=False,
        )
        self.test_department = Department.objects.create(
            name="College of Engineering, Science and Technology"
        )
        self.test_course = Course.objects.create(
            name="Mathematics",
            description="Learn plenty of mathematical skills to go into any career you want",
            department=self.test_department,
        )
        self.test_module = Module.objects.create(
            name="Mathematical Modelling",
            description="Explore how to apply MATLAB to a variety of mathematical situations",
            course=self.test_course,
            staff=self.staff_profile,
            planet_representation="",
            goals=["Draw a Lorenz Attractor using Forward Euler"],
        )
        self.test_enrolement = StudentModuleEnrolment.objects.create(
            module=self.test_module,
            student=self.temp_profile,
            enrolment_date=datetime.now(),
            enrolment_completion_date=datetime.now() + timedelta(90),
        )
        self.next_temp_user = User.objects.create(
            username="anotherUser",
            password="hello1234",
        )
        self.next_profile = StudentProfile.objects.create(
            user=self.next_temp_user,
            student_number=690923864,
            user_rank="Leiutenant",
            astro_credits=5000,
            weekly_credits=20,
            weekly_reset_date=datetime.now(),
            daily_reset_date=datetime.now(),
            favourite_module_name="Mathematical Modelling",
            first_login=False,
        )
        self.first_test_post = NetworkPosts.objects.create(
            title="Q1 Coursework Help",
            content="Do not get the second part of it do you use existence theorom",
            date_posted=datetime.now() - timedelta(5),
            author=self.next_temp_user,
            network="Mathematics Lounge",
        )
        self.first_test_post.upvote_users.set(
            [self.temp_user, self.next_temp_user])
        self.second_test_post = NetworkPosts.objects.create(
            title="Revision Structure",
            content="How are your structuring your revision",
            date_posted=datetime.now() - timedelta(3),
            author=self.temp_user,
            network="Java Lovers",
        )
        self.second_test_post.report_users.set([self.next_temp_user])
        self.first_module_post = ModulePosts.objects.create(
            module=self.test_module,
            title="Backward Euler Help",
            content="Why is it implicit I dont understand",
            date_posted=datetime.strftime(datetime.now(), "%Y-%m-%d"),
            author=self.temp_user,
        )
        self.test_network_comment = NetworkComment.objects.create(
            content = "Yes you do",
            date_posted = datetime.now(),
            author = self.temp_user,
            post = self.first_test_post,
        )
        self.test_module_comment = ModuleComment.objects.create(
            content = "Doing bit by bit",
            date_posted = datetime.now(),
            author = self.next_temp_user,
            post = self.first_module_post,
        )

    def test_start_page(self):
        response = self.client.get(self.start_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "start_page.html")

    def test_login_page(self):
        response = self.client.get(self.login_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_guest_page(self):
        response = self.client.get(self.guest_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "guest_login.html")

    def test_post_reward_overall(self):
        post_reward(self.temp_user)
        updated_profile = StudentProfile.objects.get(student_number=690923187)
        actual_credit_amount = updated_profile.astro_credits
        expected_credit_amount = 475
        self.assertEquals(expected_credit_amount, actual_credit_amount)

    def test_post_reward_weekly(self):
        post_reward(self.temp_user)
        updated_profile = StudentProfile.objects.get(student_number=690923187)
        actual_credit_amount = updated_profile.weekly_credits
        expected_credit_amount = 275
        self.assertEquals(expected_credit_amount, actual_credit_amount)

    def test_refresh_weekly_credits(self):
        refresh_weekly_credits()
        weekly_amounts = []
        first_profile = StudentProfile.objects.get(student_number=690923187)
        weekly_amounts.append(first_profile.weekly_credits)
        expected_amounts = [0]
        self.assertCountEqual(expected_amounts, weekly_amounts)

    def test_weekly_refresh_date(self):
        weekly_refresh_date()
        expected_refresh = datetime(
            datetime.now().year, datetime.now().month, datetime.now().day + 1
        )
        expected_refresh_date = datetime.strftime(expected_refresh, "%Y-%m-%d")
        first_profile = StudentProfile.objects.get(student_number=690923187)
        actual_refresh = first_profile.weekly_reset_date
        actual_refresh_date = datetime.strftime(actual_refresh, "%Y-%m-%d")
        self.assertEquals(expected_refresh_date, actual_refresh_date)

    def test_set_daily_tasks(self):
        set_daily_tasks()
        test_profile = StudentProfile.objects.get(student_number=690923187)
        amount_of_tasks = len(test_profile.daily_tasks)
        expected_amount = 3
        self.assertEquals(expected_amount, amount_of_tasks)

    def test_daily_refresh_date(self):
        daily_refresh_date()
        expected_refresh = datetime(
            datetime.now().year, datetime.now().month, datetime.now().day + 1
        )
        expected_refresh_date = datetime.strftime(expected_refresh, "%Y-%m-%d")
        test_profile = StudentProfile.objects.get(student_number=690923187)
        actual_refresh = test_profile.daily_reset_date
        actual_refresh_date = datetime.strftime(actual_refresh, "%Y-%m-%d")
        self.assertEquals(expected_refresh_date, actual_refresh_date)

    def test_get_daily_tasks(self):
        test_user = User.objects.get(username="testUser")
        actual_amount_tasks = len(get_daily_tasks(test_user))
        expected_amount_tasks = 1
        self.assertEquals(expected_amount_tasks, actual_amount_tasks)

    def test_add_personal_task(self):
        test_user = User.objects.get(username="testUser")
        add_personal_task(test_user, "Watch video to learn leapfrog method")
        predicted_tasks = [
            "Run for 10 minutes",
            "Learn to cook salad",
            "Watch video to learn leapfrog method",
        ]
        test_profile = StudentProfile.objects.get(student_number=690923187)
        actual_tasks = test_profile.personal_goals
        self.assertEqual(predicted_tasks, actual_tasks)

    def test_get_personal_task(self):
        test_user = User.objects.get(username="testUser")
        actual_tasks = get_personal_tasks(test_user)
        predicted_tasks = ["Run for 10 minutes", "Learn to cook salad"]
        self.assertEqual(predicted_tasks, actual_tasks)

    def test_set_personal_tasks(self):
        test_user = User.objects.get(username="testUser")
        set_personal_tasks(test_user, "Learn to cook salad")
        test_profile = StudentProfile.objects.get(student_number=690923187)
        actual_tasks = test_profile.personal_goals
        predicted_tasks = ["Run for 10 minutes"]
        self.assertEqual(predicted_tasks, actual_tasks)

    def test_get_long_term_goals(self):
        test_user = User.objects.get(username = "testUser")
        actual_goals = get_long_term_goals(test_user)
        test_module = Module.objects.get(name = "Mathematical Modelling")
        predicted_goals = [{
            "module": test_module,
            "goals": ["Draw a Lorenz Attractor using Forward Euler"],
        }]
        self.assertEqual(predicted_goals,actual_goals)

    def test_weekly_top_ten(self):
        actual_order = weekly_top_ten()
        predicted_order = [["testUser", 200], ["anotherUser", 20]]
        self.assertEqual(predicted_order, actual_order)

    def test_get_taught_modules(self):
        expected_modules = ["Mathematical Modelling"]
        staff_user = User.objects.get(username="testStaff")
        actual_modules = get_taught_modules(staff_user)
        self.assertEqual(expected_modules, actual_modules)

    def test_check_if_student(self):
        expected_check = True
        student_user = User.objects.get(username="anotherUser")
        actual_check = check_if_student(student_user)
        self.assertEqual(expected_check, actual_check)

    def test_get_rank_info(self):
        predicted_info = ("Rookie", "assets/rank1.svg")
        temp_user = StudentProfile.objects.get(student_number=690923187)
        credit_amount = temp_user.astro_credits
        actual_info = get_rank_info(credit_amount)
        self.assertEqual(predicted_info, actual_info)

    def test_update_ranks(self):
        temp_profile = StudentProfile.objects.get(student_number=690923187)
        temp_profile.astro_credits += 25000
        temp_profile.save()
        update_ranks()
        updated_profile = StudentProfile.objects.get(student_number=690923187)
        expected_rank = "General"
        actual_rank = updated_profile.user_rank
        self.assertEquals(expected_rank, actual_rank)

    def test_change_favourite(self):
        test_student = User.objects.get(username="testUser")
        change_favourite(test_student, "Vector Calculus and Application")
        predicted_favourite = "Vector Calculus and Application"
        test_profile = StudentProfile.objects.get(student_number=690923187)
        actual_favourite = test_profile.favourite_module_name
        self.assertEqual(predicted_favourite, actual_favourite)

    def test_find_favourite(self):
        test_user = User.objects.get(username="testUser")
        expected_favourite = "Mathematical Modelling"
        actual_favourite = find_favourite(test_user)
        self.assertEquals(expected_favourite, actual_favourite)

    def test_overall_top_ten(self):
        expected_scores = [["anotherUser", 5000], ["testUser", 400]]
        actual_scores = overall_top_ten()
        self.assertEqual(expected_scores, actual_scores)

    def test_find_all_networks(self):
        expected_networks = ["Java Lovers", "Mathematics Lounge"]
        actual_networks = find_all_networks()
        self.assertEqual(expected_networks, actual_networks)

    def test_get_student_modules(self):
        expected_modules = ["Mathematical Modelling"]
        student_user = User.objects.get(username="testUser")
        actual_modules = get_student_modules(student_user)
        self.assertEqual(expected_modules, actual_modules)

    def test_get_module_posts(self):
        expected_module_posts = [self.first_module_post]
        module_test = Module.objects.get(name="Mathematical Modelling")
        actual_module_posts = get_module_posts([module_test])
        self.assertEqual(expected_module_posts, actual_module_posts)

    def test_network_post_title(self):
        expected_title = "Q1 Coursework Help"
        test_post = NetworkPosts.objects.get(title="Q1 Coursework Help")
        actual_title = test_post.title
        self.assertEqual(expected_title, actual_title)

    def test_network_post_content(self):
        expected_content = "How are your structuring your revision"
        test_post = NetworkPosts.objects.get(
            content="How are your structuring your revision"
        )
        actual_content = test_post.content
        self.assertEqual(expected_content, actual_content)

    def test_network_post_like(self):
        predicted_upvote_amount = 2
        test_post = NetworkPosts.objects.get(title = "Q1 Coursework Help")
        actual_upvote_amount = test_post.upvote_users.count()
        self.assertEqual(predicted_upvote_amount, actual_upvote_amount)

    def test_network_post_report(self):
        predicted_report_amount = 1
        test_post = NetworkPosts.objects.get(title = "Revision Structure")
        actual_report_amount = test_post.report_users.count()
        self.assertEqual(predicted_report_amount, actual_report_amount)

    def test_academic_post_title(self):
        expected_title = "Backward Euler Help"
        test_post = ModulePosts.objects.get(id=1)
        actual_title = test_post.title
        self.assertEqual(expected_title, actual_title)

    def test_academic_post_user(self):
        predicted_username = "testUser"
        test_post = ModulePosts.objects.get(title = "Backward Euler Help")
        actual_username = test_post.author.username
        self.assertEqual(predicted_username, actual_username)
    
    def test_comments_network(self):
        predicted_comment = "Yes you do"
        test_comment = NetworkComment.objects.get(content = "Yes you do")
        commented_post = test_comment.content
        self.assertEqual(predicted_comment, commented_post)

    def test_comments_module(self):
        predicted_comment = "Doing bit by bit"
        test_comment = ModuleComment.objects.get(content = "Doing bit by bit")
        commented_post = test_comment.content
        self.assertEqual(predicted_comment, commented_post)
    
    def test_comment_network_author(self):
        predicted_author = self.temp_user
        test_comment = NetworkComment.objects.get(content = "Yes you do")
        actual_author = test_comment.author
        self.assertEqual(predicted_author, actual_author)

