from django.test import SimpleTestCase
from django.urls import reverse, resolve
from luna_application.views import *
from networks.models import NetworkPosts


class TestUrls(SimpleTestCase):
    def test_start_page_url_is_resolved(self):
        url = reverse("luna_application-start_page")
        self.assertEquals(resolve(url).func, start_page)

    def test_home_page_url_is_resolved(self):
        url = reverse("luna_application-home_page")
        self.assertEquals(resolve(url).func, home_page)

    def test_wellbeing_url_is_resolved(self):
        url = reverse("luna_application-wellbeing_tasks")
        self.assertEquals(resolve(url).func, wellbeing_tasks)

    def test_leaderboards_url_is_resolved(self):
        url = reverse("luna_application-leaderboards")
        self.assertEquals(resolve(url).func, leaderboards)

    def test_student_networks_url_is_resolved(self):
        url = reverse("luna_application-student_networks")
        self.assertEquals(resolve(url).func, student_networks)

    def test_network_display_url_is_resolved(self):
        url = reverse("luna_application-network_display")
        self.assertEquals(resolve(url).func, display_network)

    def test_academic_network_url_is_resolved(self):
        url = reverse("luna_application-academic_network")
        self.assertEquals(resolve(url).func, academic_network)

    def test_assign_tasks_url_is_resolved(self):
        url = reverse("luna_application-assign_tasks")
        self.assertEquals(resolve(url).func, assign_tasks)

    def test_module_display_url_is_resolved(self):
        url = reverse("luna_application-module_display")
        self.assertEquals(resolve(url).func, module_display)

    def test_my_profile_url_is_resolved(self):
        url = reverse("luna_application-my_profile")
        self.assertEquals(resolve(url).func, my_profile)
