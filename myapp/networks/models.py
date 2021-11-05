from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.urls import reverse

"""
    This is a table that stores every single post that
    is made on this application. There is an author
    field in the database table. This is significant
    as it will allow validation so users can only update
    and delete posts that they have created.
"""


class NetworkPosts(models.Model):
    # Title of the Post in the Network Forum
    title = models.CharField(max_length=250)
    # Text content of the post
    content = models.TextField()
    # Date the author posted the post
    date_posted = models.DateTimeField(default=timezone.now)
    # Author of the Post
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Network Forum the post was made on
    network = models.CharField(max_length=20)
    # Users that have upvoted this post
    upvote_users = models.ManyToManyField(User, related_name="users_upvote")
    # Users that have reported the post
    report_users = models.ManyToManyField(User, related_name="users_report")

    def number_of_likes(self):
        return self.upvote_users.count()

    def __str__(self):
        return self.network

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})


class NetworkComment(models.Model):
    # Module post that the network is for
    post = models.ForeignKey(
        NetworkPosts, on_delete=models.CASCADE, related_name="comments"
    )
    # Text of the comment
    content = models.TextField()
    # The date that the comment was submitted
    date_posted = models.DateTimeField(default=timezone.now)
    # Author of the comment
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Users that have upvoted this post
    upvote_users = models.ManyToManyField(
        User, related_name="network_comment_upvote")
    # Users that have reported the post
    report_users = models.ManyToManyField(
        User, related_name="network_comment_report")

    class Meta:
        ordering = ["date_posted"]

    def __str__(self):
        return str(self.post)
