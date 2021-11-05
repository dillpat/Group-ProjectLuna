from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import StaffProfile, StudentProfile


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=100000)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Module(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=100000)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE)
    goals = ArrayField(
        models.CharField(max_length=100, blank=False), size=3, default=list
    )
    planet_representation = models.CharField(
        max_length=255, default="../static/assets/planetE.svg"
    )

    def __str__(self):
        return self.name


class StudentModuleEnrolment(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    enrolment_date = models.DateField()
    enrolment_completion_date = models.DateField()

    def __str__(self):
        return self.student.user.username


class ModulePosts(models.Model):
    title = models.CharField(max_length=250)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    # Users that have upvoted this post
    upvote_users = models.ManyToManyField(
        User, related_name="module_post_upvote")
    # Users that have reported the post
    report_users = models.ManyToManyField(
        User, related_name="module_post_report")

    def __str__(self):
        return str(self.module)

    def number_of_likes(self):
        return self.upvote_users.count()

    def get_absolute_url(self):
        return reverse("module_post_detail", kwargs={"pk": self.pk})


class ModuleComment(models.Model):
    # Module post that the network is for
    post = models.ForeignKey(
        ModulePosts, on_delete=models.CASCADE, related_name="comments"
    )
    # Text of the comment
    content = models.TextField()
    # The date that the comment was submitted
    date_posted = models.DateTimeField(default=timezone.now)
    # Author of the comment
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Users that have upvoted this post
    upvote_users = models.ManyToManyField(
        User, related_name="module_comment_upvote")
    # Users that have reported the post
    report_users = models.ManyToManyField(
        User, related_name="module_comment_report")

    class Meta:
        ordering = ["date_posted"]

    def __str__(self):
        return str(self.post)
