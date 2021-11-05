from django.test import TestCase
from academics.models import Department, Course, Module, StudentModuleEnrolment, ModulePosts
from networks.models import NetworkPosts, NetworkComment
from users.models import StaffProfile, StudentProfile
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

class NetworkCommentTest(TestCase):
    def setUp(self):
        NetworkComment.objects.create(
            post = NetworkPosts.objects.create(
                title = "Computing2",
                content = "content",
                date_posted = "2021-1-3",
                author = User.objects.create(username="person8",
                                             password="Luna1234"),
                network = "AI",),

        content = "text",
        date_posted = "2021-03-1",
        author =   User.objects.create(username="person2",
                                         password="Luna1234"),)

    def test_network_comments(self):
        comment = NetworkComment.objects.get()
        self.assertEqual(comment.post.title, "Computing2")

#test for Network post, post object is created
class NetworkPostsTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(
            username="person4",
            password="Luna1234"
        )
        self.test_post = NetworkPosts.objects.create(
        title = "Computing",
        content = "content",
        date_posted = "2021-1-3",
        author = self.test_user,
        network = "AI")

    #test assert
    def test_post_network(self):
        """ Network Post is correctly identified """
        post = NetworkPosts.objects.get()
        self.assertEqual(post.title , "Computing")
        self.assertEqual(post.content, "content")
        self.assertEqual(post.author.username, "person4")
        self.assertEqual(post.network, "AI")