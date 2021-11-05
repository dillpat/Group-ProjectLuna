from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from datetime import datetime

RANK_CHOICES = (
    ("rookie", "ROOKIE"),
    ("lieutenant", "LIEUTENANT"),
    ("captain", "CAPTAIN"),
    ("colonel", "COLONEL"),
    ("general", "GENERAL"),
)

"""
    This is a table that stores every single profile that is
    created for every student user. Various information about
    student users can be stored in this table. All this
    information will be used extensively throughout the program.
"""


class StudentProfile(models.Model):
    # User that the student profile is about
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # University student number of the user
    student_number = models.IntegerField(primary_key=True)
    # Rank of the user in the application
    user_rank = models.CharField(
        max_length=10, choices=RANK_CHOICES, default="Rookie")
    # Amount of astro credits the user currently has
    astro_credits = models.IntegerField(default=0)
    # Daily wellbeing tasks that have been set for the suer
    daily_tasks = ArrayField(
        models.CharField(max_length=100, blank=False), size=3, default=list
    )
    # Amount of credit user has collected in a week
    weekly_credits = models.IntegerField(default=0)
    # Reset date for weekly credits
    weekly_reset_date = models.DateField(
        default=datetime(
            datetime.now().year, datetime.now().month, datetime.now().day + 7, 0, 0
        )
    )
    # Reset date for when daily tasks are refreshed
    daily_reset_date = models.DateField(
        default=datetime(
            datetime.now().year, datetime.now().month, datetime.now().day + 1, 0, 0
        )
    )
    # Favourite Module of the User
    favourite_module_name = models.CharField(max_length=200, default="n/a")
    # Personal Goals the user has set as part of their personal checklist
    personal_goals = ArrayField(
        models.CharField(max_length=250, blank=False), size=10, default=list
    )
    first_login = models.BooleanField(default=True)
    # The badge which shows the rank of the user
    rank_badge = models.ImageField(default="assets/rank1.svg")

    def __str__(self):
        return self.user.username


"""
    This is a table that stores every single profile that is
    created for every staff user. Various information about
    staff users can be stored in this table. All this information
    will be used extensively throughout the program.
"""


class StaffProfile(models.Model):
    # User that the staff profile is about
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # image = models.ImageField()
    # Whether they have logged into the application or not
    first_login = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
