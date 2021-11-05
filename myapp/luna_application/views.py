from operator import itemgetter
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from users.models import StaffProfile, StudentProfile
from networks.models import NetworkPosts, NetworkComment
from academics.models import StudentModuleEnrolment, ModulePosts, Module, ModuleComment
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    View,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from datetime import datetime, timedelta
import requests
import random
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages

current_network = ""
current_module = ""


def post_reward(user):
    """
        This function runs when a user posts on a
        student or academic network, so they get
        are rewarded in astro credits for posting on
        the network. The function works by storing
        every single student profile in a variable.
        The function then searches through each profile
        in this variable and finds the profile that
        consists of the user that is logged in. Astro
        credits are then added to this to the current
        total of credits they have. This change of
        data is saved in the database. This function
        is critical to the reward system as it allows
        the user to be rewarded for posting on the network.
    """
    # Storing all profiles under a variable
    all_profiles = StudentProfile.objects.all()
    # Searching through all profiles
    for each_profile in all_profiles:
        # Finding profile of the user that is logged in
        if each_profile.user == user:
            # Calculating the new amount of credits they have
            each_profile.astro_credits += 75
            each_profile.weekly_credits += 75
            print(each_profile.weekly_credits)
            # Saving the change in the database
            each_profile.save()

def network_post_like(request, pk):
    """
        This function allows a user to upvote a post.
    """
    network_post = get_object_or_404(
        NetworkPosts, id=request.POST.get("network_post_id")
    )
    if network_post.upvote_users.filter(id=request.user.id).exists():
        network_post.upvote_users.remove(request.user)
        all_profiles = StudentProfile.objects.all()
        for each_profile in all_profiles:
            if each_profile.user == request.user:
                each_profile.astro_credits -= 10
                each_profile.weekly_credits -= 10
                each_profile.save()

    else:
        network_post.upvote_users.add(request.user)

        # Find Student Profile of the User
        all_profiles = StudentProfile.objects.all()
        for each_profile in all_profiles:
            if each_profile.user == request.user:
                each_profile.astro_credits += 10
                each_profile.weekly_credits += 10
                each_profile.save()

    return HttpResponseRedirect(reverse("post_detail", kwargs={"pk": pk}))


def network_post_report(request, pk):
    """
        This function allows a user to report a post.
    """
    network_post = get_object_or_404(
        NetworkPosts, id=request.POST.get("network_report_id")
    )
    if network_post.report_users.filter(id=request.user.id).exists():
        network_post.report_users.remove(request.user)
    else:
        network_post.report_users.add(request.user)

    if network_post.report_users.count() >= 5:
        network_post.delete()
        return HttpResponseRedirect(reverse("luna_application-network_display"))

    return HttpResponseRedirect(reverse("post_detail", kwargs={"pk": pk}))


# def refresh_weekly_credits():
#     all_profiles = StudentProfile.objects.all()
#     for every_profile in all_profiles:
#         every_profile.weekly_credits = 0
#         each_profile.save()
#
#
# def weekly_refresh_date():
#     new_reset_time = datetime(
#         datetime.now().year, datetime.now().month, datetime.now().day + 1, 0, 0
#     )
#     all_profiles = StudentProfile.objects.all()
#     for each_profile in all_profiles:
#         each_profile.weekly_reset_date = new_reset_time
#         each_profile.save()
#
#
# def refresh_weekly_credits():
#     all_profiles = StudentProfile.objects.all()
#     for every_profile in all_profiles:
#         every_profile.weekly_credits = 0


# def weekly_refresh_date():
#     new_reset_time = datetime(
#         datetime.now().year, datetime.now().month, datetime.now().day + 1, 0, 0
#     )
#     all_profiles = StudentProfile.objects.all()
#     for each_profile in all_profiles:
#         each_profile.weekly_reset_date = new_reset_time


# def reset_weekly_credits(current_user):
#     # Finding student profile
#     all_profiles = StudentProfile.objects.all()
#     for each_profile in all_profiles:
#         if each_profile.user == all_profiles:
#             reset_date = each_profile.weekly_reset_date
#             if datetime.now() > reset_date:
#                 refresh_weekly_credits()
#                 daily_refresh_date()





def start_page(request):
    """
        This function represents the link between
        the url of the starting page of the application
        to the HTML template. The template is returned
        in this function and the contents of this template
        is displayed for the URL which is linked to this
        function in urls.py.
    """
    return render(request, "start_page.html")





def login_page(request):
    """
        This function represents the link between
        the url of the login page of the application
        to the HTML template. The template is returned
        in this function and the contents of this template
        is displayed for the URL which is linked to this
        function in urls.py.
    """
    return render(request, "login.html")


def guest_login(request):
    """
        This function represents the link between
        the url of the guest page of the application
        to the HTML template. The template is returned
        in this function and the contents of this template
        is displayed for the URL which is linked to this
        function in urls.py.
    """
    return render(request, "guest_login.html")




def get_article_info():

    """
        This function is run every time the
        wellbeing page is opened in the applicaton.
        The function uses a news api to access the
        latest news articles about wellbeing.
        At the end of the function a 2D array is returned
        where each array consists the title, URL and URL of
        an image of an article.This function is important
        as this allows one of the main sources of wellbeing
        aid to students through these news articles being
        produced.
    """
    api_key = "e90c5bb44fd5421eacd2be534fd36f80"
    # Parameters that allow us to access the relevant articles
    params = {
        "q": "self-help",
        "apiKey": api_key,
    }
    headers = {
        "X-Api-Key": api_key,  # KEY in header to hide it from url
    }
    # URL that allows us to access the relevant articles
    url = "https://newsapi.org/v2/everything?q=fitness&apiKey=e90c5bb44fd5421eacd2be534fd36f80"
    # Request the required data that is required
    response = requests.get(url, params=params, headers=headers)
    # Storing the required data in a dictionary
    data = response.json()
    # Storing the required data in an array
    articles = data["articles"]
    # Searching through the data for the information we require and storing it in an array
    article_info = []
    for arr in articles:
        # Array created to store info about one article
        one_article = []
        # Storing the title of the article
        one_article.append(arr["title"])
        # Storing the URL of the article
        one_article.append(arr["url"])
        # Storing the URL of one of the images that may be in the article
        one_article.append(arr["urlToImage"])
        # Adding all the info about this article to a storage of all the articles
        article_info.append(one_article)

    return article_info




def get_required_articles():
    """
        This function is executed every time the wellbeing
        page is accessed on the application. On the wellbeing
        page there are only information about four articles
        displayed. Therefore this function chooses four articles
        from all the articles randomly and stores this in a new
        array. This array is returned and used in a template
        so information about these articles are displayed on the
        wellbeing page.
    """
    # Using a function above to call the latest information about current articles
    our_info = get_article_info()
    article_amount = len(our_info) - 1
    # Chooses four articles randomly
    article_numbers = random.sample(range(1, article_amount), 4)

    # Store information about the articles that have been randomly chosen
    required_articles = []
    # Finding the articles that have been randomly chosen and storing the
    # required information about them
    for j in article_numbers:
        required_articles.append(our_info[j])

    # Returing information about the articles that have been randomly chosen
    return required_articles


def set_the_task(module_selected, task_to_set):
    """
    This function assignes the task for the requested module

    """
    all_modules = Module.objects.all()
    for each_module in all_modules:
        if each_module.name == module_selected:
            each_module.goals.append(task_to_set)
            each_module.save()


def refresh_weekly_credits():
    """
    This function resets all weekly credits earned fro every student
    """
    all_profiles = StudentProfile.objects.all()
    for every_profile in all_profiles:
        every_profile.weekly_credits = 0
        every_profile.save()


def weekly_refresh_date():
    """
    This function assigns the users refresh date. This is done to all student
    profiles
    """
    new_reset_time = datetime(
        datetime.now().year, datetime.now().month, datetime.now().day + 1, 0, 0
    )
    all_profiles = StudentProfile.objects.all()
    for each_profile in all_profiles:
        each_profile.weekly_reset_date = new_reset_time
        each_profile.save()


def reset_weekly_credits(current_user):
    """
    This function resets the weekly credit dates, from when valid credits can be
    gained.
    """
    # Finding student profile
    all_profiles = StudentProfile.objects.all()
    for each_profile in all_profiles:
        if each_profile.user == current_user:
            reset_date = each_profile.weekly_reset_date
            proper_reset_date = datetime.strftime(reset_date, "%Y-%m-%d")
            now_date = datetime.strftime(datetime.today(), "%Y-%m-%d")
            if now_date >= proper_reset_date:
                refresh_weekly_credits()
                weekly_refresh_date()
                break


def home_page(request):
    """
        This function represents the URL and the template
        for the home page of the application. The template
        that is returned is based on whether the user enters
        the correct login details.
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    # Possibly resetting weekly credits
    reset_weekly_credits(request.user)
    user_terms = None
    if request.method == "POST":
        if request.POST.get("terms_accepted"):
            all_profiles = StudentProfile.objects.all()
            for each_profile in all_profiles:
                if each_profile.user == request.user:
                    user_terms = get_object_or_404(
                        StudentProfile, user_id=request.user.id
                    )
            if user_terms == None:
                user_terms = get_object_or_404(
                    StaffProfile, user_id=request.user.id)
            user_terms.first_login = False
            user_terms.save()
            return redirect("../password_reset/")

        if request.POST.get("declined"):
            return redirect("../login/")


    terms = None

    all_profiles = StudentProfile.objects.all()
    for each_profile in all_profiles:
        if each_profile.user == request.user:
            terms = each_profile.first_login
            planet_img = find_planet_image(
                StudentProfile.objects.filter(user=request.user)[0]
            )

    if terms == None:
        staff_profiles = StaffProfile.objects.all()
        for every_profile in staff_profiles:
            if every_profile.user == request.user:
                terms = every_profile.first_login
                planet_img = "../static/assets/planetE.svg"

    return render(
        request,
        "home_page.html",
        {
            "policy": terms,
            "fav_planet": planet_img,
        },
    )


def find_planet_image(current_user):
    """
    This function identifies the planet img corresponding to the users favourite
    module

    """
    favourite_module_name = current_user.favourite_module_name
    favourite_module = Module.objects.get(name=favourite_module_name)
    planet_image = favourite_module.planet_representation
    return planet_image


def set_daily_tasks():
    """
    This function sets the users daily tasks from the implmented list below,
    and a random 3 are selected to be completed for every student
    """
    # Possible wellbeing tasks you can set for students
    possible_tasks = [
        "Read for 10 minutes",
        "Go for a 15 minute run",
        "Go for a 15 minute walk",
        "Read a wellbeing article",
        "Eat a healthy snack",
        "Talk to a friend about a current news topic",
        "Meditate for 10 minutes",
        "Stretch for 5 minutes",
        "Go for a 15 minute bike ride",
        "Do a breathing exercise for 2 minutes",
        "Eat an apple",
        "Eat an orange",
        "Listen to your favourite song",
        "Meet up with a friend",
        "Order your favourite food",
        "Drink a litre of water",
        "Drink a glass of water",
        "Eat a banana",
        "Talking to coursemate about a module",
    ]

    # Assigning wellbeing tasks to all students randomly
    all_profiles = StudentProfile.objects.all()
    for each_profile in all_profiles:
        each_profile.daily_tasks = random.sample(possible_tasks, 3)
        each_profile.save()


def daily_refresh_date():
    """
    This function sets the refresh time for the dailty tasks

    """
    new_reset_time = datetime(
        datetime.now().year, datetime.now().month, datetime.now().day + 1, 0, 0
    )
    all_profiles = StudentProfile.objects.all()
    for each_profile in all_profiles:
        each_profile.daily_reset_date = new_reset_time
        each_profile.save()


def reset_daily_tasks(current_user):
    """
    This function resets the users daily tasks, as the timeset will have updated
    The times are updated for the user, where the relevant functions identify
    if the users daily tasks need to be updated.
    """
    # Finding student profile
    all_profiles = StudentProfile.objects.all()
    for each_profile in all_profiles:
        if each_profile.user == current_user:
            reset_date = each_profile.daily_reset_date
            proper_reset_date = datetime.strftime(reset_date, "%Y-%m-%d")
            now_date = datetime.strftime(datetime.today(), "%Y-%m-%d")
            if now_date >= proper_reset_date:
                set_daily_tasks()
                daily_refresh_date()
                break


def get_daily_tasks(current_user):
    """
        This function is executed everytime the wellbeing
        page is opened on the application. The function
        searches through the table of student profiles to
        find the daily tasks of the user that is currently
        logged in. This is so it can be displayed on the
        template. This function is called in the function
        wellbeing_tasks.
    """
    # Storing every object about every student profile in a variable
    all_profiles = StudentProfile.objects.all()
    # Searching for the profile of the user that is currently logged in
    for each_profile in all_profiles:
        if each_profile.user == current_user:
            current_profile = each_profile
    # Accessing the daily wellbeing tasks of the user that is currently logged in
    tasks_daily = current_profile.daily_tasks
    # The daily wellbeing tasks of the user that is logged in are returned in
    if len(tasks_daily) == 0:
        tasks_daily.append("DONE")

    return tasks_daily


def daily_goal_reward(current_user):
    """
        This function represents the link between the
        URL and the template for the wellbeing page.
        Various functions are called from above and
        the contents that is returned from these functions
        are passed to the template that is returned at the
        end.
    """
    all_profiles = StudentProfile.objects.all()
    for each_profile in all_profiles:
        if each_profile.user == current_user:
            each_profile.astro_credits += 10
            each_profile.weekly_credits += 10
            each_profile.save()
            print(each_profile.astro_credits)
            print(each_profile.weekly_credits)
            break


def add_personal_task(current_user, new_user_task):
    """
    This function gets a user object and finds the user form the Student profiles
    database. The new string task is appened to the new usr taks list.
    The users new personal goals are then updated and saved.
    """
    current_personal = []
    all_profiles = StudentProfile.objects.all()
    for each_profile in all_profiles:
        if each_profile.user == current_user:
            current_personal = each_profile.personal_goals
            current_personal.append(new_user_task)
            each_profile.personal_goals = current_personal
            each_profile.save()





def get_personal_tasks(current_user):
    """
    This function gets a user obect and finds the user form the Student profiles
    database, and retrives the users personal tasks from the database.
    The string array is returned
    """
    all_profiles = StudentProfile.objects.all()
    for each_profile in all_profiles:
        if each_profile.user == current_user:
            tasks_personal = each_profile.personal_goals

    return tasks_personal


def set_personal_tasks(current_user, goal_to_remove):
    """
    This function updates the personal tasks for the user.
    When the user ticks off their personal task, the users personal tasks
    will be updated
    """
    all_profiles = StudentProfile.objects.all()
    for each_profile in all_profiles:
        if each_profile.user == current_user:
            current_goals = each_profile.personal_goals
            for task in current_goals:
                if task == goal_to_remove:
                    current_goals.remove(goal_to_remove)
            each_profile.personal_goals = current_goals
            each_profile.save()


def update_daily_tasks(request):
    """
    This function updates the current daily task for the user.
    When the use ticks off the task the task will be removed, with credits
    added to the users profile
    """
    text = request.GET.get("taskName")
    current_user = request.user
    all_profiles = StudentProfile.objects.all()
    for each_profile in all_profiles:
        if each_profile.user == current_user:
            tasks_daily = each_profile.daily_tasks
            for task in tasks_daily:
                if task == text:
                    tasks_daily.remove(text)
                    each_profile.astro_credits += 10
                    each_profile.weekly_credits += 10
                    each_profile.save()
            each_profile.daily_tasks = tasks_daily
            each_profile.save()

    daily_tasks = get_daily_tasks(current_user)
    # Accessing Long Term Goals of the User
    long_term_goals = get_long_term_goals(current_user)
    # Accessing Relevant Wellbeing Articles
    articles_display = get_required_articles()
    # Setting Daily Wellbeing Tasks
    reset_daily_tasks(current_user)
    # Getting User Set Tasks
    personal_tasks = get_personal_tasks(current_user)
    return render(
        request,
        "wellbeing_tasks.html",
        {
            "daily_tasks": daily_tasks,
            "articles_display": articles_display,
            "long_term_goals": long_term_goals,
            "personal_tasks": personal_tasks,
        },
    )


def get_user_task(request):
    """
    This function retrives the users personal tasks from the user request for the
    wellbeing page
    """
    text = request.GET.get("taskName")
    current_user = request.user
    personal_tasks = get_personal_tasks(current_user)
    for task in personal_tasks:
        if text == task:
            set_personal_tasks(current_user, text)
    # Getting User Set Tasks
    personal_tasks = get_personal_tasks(current_user)
    return personal_tasks


def wellbeing_tasks(request):
    """
    This function uses user requst data to diplay the users wellbeing page.
    The user's personal,daily and long term tasks are set and retrived.
    The user can make a post request to update their personal tasks.
    Api artiles are fetched from the get_required_articles() function.
    The json data is parsed to the wellbeing html page.
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    # Getting the user that is currently logged in
    current_user = request.user
    if request.method == "POST":
        new_user_task = request.POST.get("new_personal_task")
        if new_user_task == "":
            daily_tasks = get_daily_tasks(current_user)
            # Accessing Long Term Goals of the User

            long_term_goals = get_long_term_goals(current_user)
            # Accessing Relevant Wellbeing Articles
            articles_display = get_required_articles()
            # Setting Daily Wellbeing Tasks
            reset_daily_tasks(current_user)
            # Getting User Set Tasks
            personal_tasks = get_personal_tasks(current_user)
            return render(
                request,
                "wellbeing_tasks.html",
                {
                    "daily_tasks": daily_tasks,
                    "articles_display": articles_display,
                    "long_term_goals": long_term_goals,
                    "personal_tasks": personal_tasks,
                },
            )
        else:
            add_personal_task(current_user, new_user_task)
    # Accessing Daily Tasks of the User
    daily_tasks = get_daily_tasks(current_user)
    # long term goals for the user

    long_term_goals = get_long_term_goals(current_user)
    # Accessing Relevant Wellbeing Articles
    articles_display = get_required_articles()
    # Setting Daily Wellbeing Tasks
    reset_daily_tasks(current_user)
    # Getting User Set Tasks
    personal_tasks = get_personal_tasks(current_user)
    # HTML template is returned
    # Wellbeing tasks, information about latest articles
    # and long term goals of the user that has logged in
    # are passed to the template
    # print(long_term_goals)
    return render(
        request,
        "wellbeing_tasks.html",
        {
            "daily_tasks": daily_tasks,
            "articles_display": articles_display,
            "long_term_goals": long_term_goals,
            "personal_tasks": personal_tasks,
        },
    )


def get_long_term_goals(current_user):
    """
        This function searches through the module
        enrolements to find the modules that the student
        has logged in are enrolled to. Then these modules
        are searched through in a seperate table to access
        the goals for these modules. These are all then
        added to an array and returned at the end of the
        function. This function is executed before the
        wellbeing page is opened.
    """
    long_term_goals = []
    all_enrolements = StudentModuleEnrolment.objects.all()
    for each_enrolement in all_enrolements:
        if each_enrolement.student.user == current_user:
            module = {}
            module["module"] = each_enrolement.module
            module["goals"] = each_enrolement.module.goals
            long_term_goals.append(module)
    return long_term_goals


def weekly_top_ten():
    """
    This function selects the weekly top ten users with the highest credit score
    for the week. The users are then ranked in order for the leaderboard.
    """
    # Storing each student profile object in a variable
    all_profiles = StudentProfile.objects.all()
    # Get Current Astro Credit Scores for each User
    current_scores = []
    for each_profile in all_profiles:
        user_section = []
        user_section.append(each_profile.user.username)
        user_section.append(each_profile.weekly_credits)
        current_scores.append(user_section)
    # Sorting Array based on the amount of astro credits
    sorted_scores = sorted(current_scores, key=itemgetter(1))[::-1]
    # Storing Top 10 users
    weekly_top_scores = []
    if len(sorted_scores) > 10:
        for i in range(10):
            weekly_top_scores.append(sorted_scores[i])
    else:
        weekly_top_scores = sorted_scores

    return weekly_top_scores


def overall_top_ten():
    """
    This function selects the overall top ten users with the highest credit score
    for the week. The users are then ranked in order for the leaderboard.
    """
    # Storing each student profile object in a variable
    all_profiles = StudentProfile.objects.all()
    # Get Current Astro Credit Scores for each User
    current_scores = []
    for each_profile in all_profiles:
        user_section = []
        user_section.append(each_profile.user.username)
        user_section.append(each_profile.astro_credits)
        current_scores.append(user_section)
    # Sorting Array based on the amount of astro credits
    sorted_scores = sorted(current_scores, key=itemgetter(1))[::-1]
    # Storing Top 10 users
    top_scores = []
    if len(sorted_scores) > 10:
        for i in range(10):
            top_ten_scores.append(sorted_scores[i])
    else:
        top_scores = sorted_scores

    return top_scores


def leaderboards(request):
    """
        This function represents the link between the
        URL and the template for the leaderboards page
        on the application. The function finds the top
        ten users in terms of astro credits. These are
        users are then stored with their amounts of astro
        credits. These are then passed to the tempalte that
        is returned at the end of the function.
    """
    # Returns another template to users that are not logged in
    # This way URL's cannot be accessed where students are not
    # logged in
    if not request.user.is_authenticated:
        return render(request, "login.html")
    # reset_weekly_amount()
    weekly_scores = weekly_top_ten()
    overall_scores = overall_top_ten()
    # Passing the top 10 users and their scores to a template and returning it
    return render(
        request,
        "leaderboards.html",
        {
            "top_scores": overall_scores,
            "weekly_scores": weekly_scores,
        },
    )

def find_all_networks():
    """
        All networks that are in the database are retrived
    """
    # To store all student networks that currently exist
    networks = []
    # Calling every object about every post on every student network
    all_networks = NetworkPosts.objects.all()
    # Searching through each student network post object
    for network in all_networks:
        # Adding all student networks where there is a post aobut them
        if str(network) not in networks:
            networks.append(str(network))
            networks.sort()
    return networks



def student_networks(request):
    """
        The function represents the link between the URL
        and the template for the student networks page on
        the application. All the student networks that
        currently exists are accessed and passed to a
        template that is returned at the end of the
        function.
    """
    # Template for login page is returned if user is not logged in
    if not request.user.is_authenticated:
        return render(request, "login.html")
    all_networks = find_all_networks()
    context = {"networks": all_networks}
    # Passing all student networks where there is a post about them to a template
    # Returning the template
    return render(request, "student_networks.html", context)



class network_create_view(CreateView, LoginRequiredMixin):
    """
        This function allows the user to create a
        student network.
    """
    model = NetworkPosts
    fields = ["network"]
    template_name = "create_network.html"

    def form_valid(self, form):
        # Accesses the user that is currently returned in
        form.instance.author = self.request.user
        return super().form_valid(form)



def display_network(request):
    """
        This function represents the link between the URL
        and the template of the page that displays forums
        of a student network.
    """
    # Stops a user that is not logged in viewing this material
    if not request.user.is_authenticated:

        return render(request, "login.html")
    # Calling the network that the user wanted to view
    if request.method == "POST":
        global current_network
        current_network = request.POST["network"]

    # Calls every single student network post object
    # Objects are stored in the variable in descending order in terms of the date posted
    required_posts = NetworkPosts.objects.filter(network=current_network).order_by(
        "-date_posted"
    )
    users = StudentProfile.objects.all()
    context = {"posts": required_posts, "users": users}
    # Passes the posts about on the network chosen by the user to the template
    return render(request, "network_display.html", context)



class post_detail_view(DetailView):
    """
        This class allows a user to look at a post on a
        student network just singurlaly on a page on its
        own. Also on this page you will have options to
        edit the post and delete the post. This class
        also represents the link between the template
        and the URL for looking at any post on a student
        network individually.
    """
    model = NetworkPosts
    template_name = "single_post.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        network_post = get_object_or_404(NetworkPosts, id=self.kwargs["pk"])
        if network_post.report_users.count() >= 5:
            network_post.delete()
            return None
        else:
            liked = False
            reported = False
            if network_post.upvote_users.filter(id=self.request.user.id).exists():
                liked = True
            if network_post.report_users.filter(id=self.request.user.id).exists():
                reported = True
            relevant_comments = []
            all_comments = NetworkComment.objects.all()
            for each_comment in all_comments:
                if each_comment.post == network_post:
                    relevant_comments.append(each_comment)

            data["number_of_likes"] = network_post.number_of_likes()
            data["post_is_liked"] = liked
            data["post_is_reported"] = reported
            data["comments"] = relevant_comments
            return data


def network_post_comment(request, pk):
    """
    This function allows a user to comment on a network post
    """
    if request.method == "POST":
        comment_made = request.POST.get("comment_posted")
        network_post = NetworkPosts.objects.get(id=pk)
        network_comment = NetworkComment.objects.create(
            post=network_post,
            content=comment_made,
            date_posted=datetime.now(),
            author=request.user,
        )
        network_comment.save()
        if check_if_student(request.user) == True:
            current_profile = StudentProfile.objects.get(user = request.user)
            current_profile.astro_credits += 20
            current_profile.weekly_credits += 20
            current_profile.save()
    return HttpResponseRedirect(reverse("post_detail", kwargs={"pk": pk}))


def module_post_comment(request, pk):
    """
    This function allows a user to comment on a module post
    """
    if request.method == "POST":
        comment_made = request.POST.get("comment_posted")
        module_post = ModulePosts.objects.get(id=pk)
        module_comment = ModuleComment.objects.create(
            post=module_post,
            content=comment_made,
            date_posted=datetime.now(),
            author=request.user,
        )
        module_comment.save()
        if check_if_student(request.user) == True:
            current_profile = StudentProfile.objects.get(user = request.user)
            current_profile.astro_credits += 20
            current_profile.weekly_credits += 20
            current_profile.save()
    return HttpResponseRedirect(reverse("module_post_detail", kwargs={"pk": pk}))


def module_post_like(request, pk):
    """
    This function allows user to like posts made in the academic module pages
    """
    module_post = get_object_or_404(
        ModulePosts, id=request.POST.get("module_post_id"))
    if module_post.upvote_users.filter(id=request.user.id).exists():
        module_post.upvote_users.remove(request.user)
        all_profiles = StudentProfile.objects.all()
        for each_profile in all_profiles:
            if each_profile.user == request.user:
                each_profile.astro_credits -= 10
                each_profile.weekly_credits -= 10
                each_profile.save()
    else:
        module_post.upvote_users.add(request.user)

        # Find Student Profile of the User
        all_profiles = StudentProfile.objects.all()
        for each_profile in all_profiles:
            if each_profile.user == request.user:
                each_profile.astro_credits += 10
                each_profile.weekly_credits += 10
                each_profile.save()

    return HttpResponseRedirect(reverse("module_post_detail", kwargs={"pk": pk}))


def module_post_report(request, pk):
    """
    This function allows users to report a post in the academic module pages
    """
    module_post = get_object_or_404(
        ModulePosts, id=request.POST.get("module_report_id")
    )
    if module_post.report_users.filter(id=request.user.id).exists():
        module_post.report_users.remove(request.user)
    else:
        module_post.report_users.add(request.user)

    if module_post.report_users.count() >= 5:
        module_post.delete()
        return HttpResponseRedirect(reverse("luna_application-module_display"))

    return HttpResponseRedirect(reverse("module_post_detail", kwargs={"pk": pk}))



class post_create_view(CreateView, LoginRequiredMixin):
    """
        This class represents the link between the URL and
        the template for being able to create a post on
        a student network on the application.
    """
    # Database model we are accessing
    model = NetworkPosts
    # Fields in the table we are accessing
    fields = ["title", "content"]
    # Template where information is going to be displayed
    template_name = "create_post.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.network = current_network
        post_reward(self.request.user)
        return super().form_valid(form)



class post_update_view(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
        This class represents the link between the URL
        and the template for the page where you are able
        to update a post on a student network. There is
        also validation in place so students that have
        logged in can only update a post. Further to this,
        there is validation that students can only update posts
        that they have previously posted.
    """
    # Database model we are accessing
    model = NetworkPosts
    # Fields in the table we are accessing
    fields = ["title", "content"]
    # Template where information is going to be displayed
    template_name = "create_post.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class post_delete_view(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
        This class represents the link between the URL and the
        template for the page wehre you are able to delete a post
        on a student network. There is also validation in palce so
        students that ahve logged in can only delete a post. Futher,
        to this, there is valdiation that students can only delete
        posts that they themselves have previously posted.
    """
    model = NetworkPosts
    template_name = "post_confirm_delete.html"
    success_url = "/network_display"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def get_student_modules(current_user):
    """
    This function gets all the modules that the user is enrolled on.
    """
    modules = []
    # Accessing all modules that students are enrolled onto
    all_student_enrolment = StudentModuleEnrolment.objects.all()
    # Searching through all student enrolement objects
    for module in all_student_enrolment:
        # Finding modules that the user that is logged on are enrolled
        if module.student.user == current_user:
            if module.module.name not in modules:
                # Storing modules that the logged on user is enrolled onto
                modules.append(module.module.name)
                modules.sort()
    return modules


def academic_network(request):
    """
        This function allows all the modules
        that the user is part enrolled displayed
        so the user can post on these academic
        networks. The function finds the user that
        is logged in and then finds all the modules
        that the user is enrolled onto. The function
        handles whether the user is a staff or a
        student and the opportunities displayed on
        the UI are dependent on this. The modules
        that the student and staff are part of are
        passed to a template that is returned at
        the end of the function.
    """
    if not request.user.is_authenticated:
        return render(request, "login.html")

    if check_if_student(request.user) == False:
        current_user = request.user
        staff_modules = get_taught_modules(current_user)
        context = {"modules": staff_modules}
        # Passing the modules to a template and returning it
        return render(request, "academic_network.html", context)

    else:
        current_user = request.user
        student_modules = get_student_modules(current_user)
        print(student_modules)
        context = {"modules": student_modules}
        # Passing the modules and returning the template at the end of the function
        return render(request, "academic_network.html", context)


def get_module_posts(current_module):
    """
    This function gets the posts made in the modules. These are ordered by the
    date the post was created
    """
    # Storing all academic network posts in a variable in order of date
    all_posts = ModulePosts.objects.all().order_by("-date_posted")

    posts = []
    # Searching through all the posts
    for post in all_posts:
        # Checking if these posts are posts of the network the user wants to see
        if str(post.module) == current_module[0].name:
            # Storing the posts we are interested in
            posts.append(post)
    return posts


def module_display(request):
    """
        This function allows posts on an academic network to
        be displayed. The function catches the academic network
        the user selects and finds all the post objects for that
        network. These are then passed to a template at the end
        of the function which are displayed.
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":
        global current_module

    # Finding all the posts for the module the user has selected
    current_module = Module.objects.filter(name=request.POST["module"])
    module_posts = get_module_posts(current_module)
    context = {"posts": module_posts}
    # Passing the posts we have found to a template that is returned
    return render(request, "module_display.html", context)


def get_taught_modules(current_user):
    """
    This function retrives the modules that are taught by the staff user
    """
    modules_taught = []
    all_modules = Module.objects.all()
    for each_module in all_modules:
        if each_module.staff.user == current_user:
            modules_taught.append(each_module.name)
    return modules_taught


def assign_tasks(request):
    """
    This function assigns the user tasks for the module that is selected by the user.
    These tasks are created bu staff, and assigned to the module.
    """
    current_user = request.user
    taught_modules = get_taught_modules(current_user)
    if request.method == "POST":
        module_selected = request.POST.get("selected_module")
        task_to_set = request.POST["task_set"]
        set_the_task(module_selected, task_to_set)
    return render(request, "assign_tasks.html", {"taught_modules": taught_modules})


class module_post_detail_view(DetailView):
    """
        This class allows a user to look at a post on an
        academic network just singurlaly on a page on its
        own. Also on this page you will have options to
        edit the post and delete the post. This class
        also represents the link between the template
        and the URL for looking at any post on an academic
        network individually.
    """
    # Accessing database which constists of every academic post
    model = ModulePosts
    # Template where the infomation is being sent too
    template_name = "module_single_post.html"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        module_post = get_object_or_404(ModulePosts, id=self.kwargs["pk"])
        if module_post.report_users.count() >= 5:
            module_post.delete()
            return None
        else:
            liked = False
            reported = False
            if module_post.upvote_users.filter(id=self.request.user.id).exists():
                liked = True
            if module_post.report_users.filter(id=self.request.user.id).exists():
                reported = True
            relevant_comments = []
            all_comments = ModuleComment.objects.all()
            for each_comment in all_comments:
                if each_comment.post == module_post:
                    relevant_comments.append(each_comment)

            data["number_of_likes"] = module_post.number_of_likes()
            data["post_is_liked"] = liked
            data["post_is_reported"] = reported
            data["comments"] = relevant_comments
            return data


def check_if_student(this_user):
    """
        This function looks through all the the student profile
        objects for the profile of the user that is currently
        logged in. If this is not found this means that the user
        that is currently logged in is not a student. This will
        effect the material that will be viewed on the web page.
        The result of this check is returned at the end of the
        function.
    """
    is_student = None
    # Stores each student profile object in a variable
    all_student_profiles = StudentProfile.objects.all()
    # Searches through all the student profile objects
    for each_student in all_student_profiles:
        # Finds the profile of the user that is currently logged in
        if each_student.user == this_user:
            # Student profile found so currently logged in user is a student
            is_student = True
            break
        else:
            # Student profile not found so currently logged in user is not a student
            is_student = False
    # Result of check is returned
    return is_student


class module_post_create_view(CreateView, LoginRequiredMixin):
    """
        This class represents the link between the URL and
        the template for being able to create a post on
        a academic network on the application.
    """
    # Database module we are accessing
    model = ModulePosts
    # Fields in the database we are accessing
    fields = ["title", "content"]
    # Template where the infomation will be displayed
    template_name = "create_post.html"
    # Order by most recent post
    ordering = ["-date_posted"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.module = current_module[0]
        if check_if_student(self.request.user) == True:
            post_reward(self.request.user)
        return super().form_valid(form)

class module_post_update_view(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
        This class represents the link between the URL
        and the template for the page where you are able
        to update a post on an academic network. There is
        also validation in place so students that have
        logged in can only update a post. Further to this,
        there is validation that students can only update posts
        that they have previously posted.
    """
    # Database module we are accessing
    model = ModulePosts
    # Fields in the database we are accessing
    fields = ["title", "content"]
    # Template where the infomation will displayed
    template_name = "create_post.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.module = current_module[0]
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class module_post_delete_view(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
        This class represents the link between the URL
        and the template for the page where you are able
        to update a post on an academic network. There is
        also validation in place so students that have
        logged in can only update a post. Further to this,
        there is validation that students can only update posts
        that they have previously posted.
    """
    model = ModulePosts
    template_name = "module_post_confirm_delete.html"
    success_url = "/module_display"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def get_rank_info(credit_amount):
    """
        This function takes a certain amount of astro
        credits and returns what rank the user is. This
        function is run every time the profile of the user
        is opened so if the user's rank has changed they will
        see it.
    """
    # Information about each Rank
    rank_info = {
        "General": {"credits_required": 25000, "badge": "assets/rank5.svg"},
        "Colonel": {"credits_required": 15000, "badge": "assets/rank4.svg"},
        "Captain": {"credits_required": 8000, "badge": "assets/rank3.svg"},
        "Lieutenant": {"credits_required": 4000, "badge": "assets/rank2.svg"},
        "Rookie": {"credits_required": -1, "badge": "assets/rank1.svg"},
    }
    # Array that has each rank
    POSSIBLE_RANKS = ["General", "Colonel", "Captain", "Lieutenant", "Rookie"]

    # Finding which rank and the corresponding badge
    for each_rank in POSSIBLE_RANKS:
        if credit_amount >= rank_info[each_rank]["credits_required"]:
            final_rank = each_rank
            final_badge = rank_info[each_rank]["badge"]
            break
        # Rank calculated is passed at the end of the function
    return final_rank, final_badge


def update_ranks():
    """
        This function searches through all the students profiles
        that currently exist. It accesses the amount of astro credits
        they currently have and calculates the corresponding rank
        they have. This is then stored in the database.
    """
    # Storing every single student profile object in a variable
    all_profiles = StudentProfile.objects.all()
    # Searching through all the student profiles
    for each_profile in all_profiles:
        # Accessing the amount of astro credits every student has
        credit_amount = each_profile.astro_credits
        user_rank_info = get_rank_info(credit_amount)
        # Storing the new rank in the database in their profile
        each_profile.user_rank = user_rank_info[0]
        each_profile.rank_badge = user_rank_info[1]
        # Saving this change in the database
        each_profile.save()





def change_favourite(current_user, new_favourite):
    """
        This function represents the link between the URL
        and the template for the profile page on the
        application. The function uses function above
        to access information about the user and calls these
        functions so this information on the profile page.
        This information is passed to the template which
        is returned at the end of the function.
    """
    all_profiles = StudentProfile.objects.all()
    for each_profile in all_profiles:
        if each_profile.user == current_user:
            each_profile.favourite_module_name = str(new_favourite)
            each_profile.save()


def find_favourite(current_user):
    """
    Function uses request data for the correct user favourite module.
    This will be use for the update for the planet homepage, where the centre
    planet will be updated accordingly for the module selected.
    """
    all_profiles = StudentProfile.objects.all()
    for each_profile in all_profiles:
        if each_profile.user == current_user:
            user_favourite = each_profile.favourite_module_name
    return user_favourite


def my_profile(request):
    """
        This function represents the link between the URL
        and the template for the profile page on the
        application. The function uses function above
        to access information about the user and calls these
        functions so this information on the profile page.
        This information is passed to the template which
        is returned at the end of the function.
    """
    if check_if_student(request.user) == True:
        # Stops students that have not logged in viewing this material
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
        if request.method == "POST":
            current_user = request.user
            new_favourite = request.POST.get("selected_favourite")
            change_favourite(current_user, new_favourite)
        # Getting all the enrolements
        all_enrolements = StudentModuleEnrolment.objects.all()
        # Find the user that is logged in
        current_user = request.user
        # Find modules that the student that has logged in has enrolled to
        modules = []
        # Searching through each student enrolement to each module
        for every_enrolement in all_enrolements:
            # Finds modules that the user that is currently logged in are enrolled onto
            if every_enrolement.student.user == current_user:
                # Accessing the data about a module that this student is enrolled onto
                this_module = every_enrolement.module
                # Accessing the name of the module that this student is enrolled onto
                module_name = this_module.name
                # Storing the names of the modules that students are enrolled onto
                modules.append(module_name)

        # Changes any ranks of students that need to be changed
        update_ranks()
        all_profiles = StudentProfile.objects.all()
        displayed_module = ""
        for each_profile in all_profiles:
            if each_profile.user == request.user:
                displayed_module = find_favourite(current_user)
        # Modules that the student study is passed to a template that is returned

        return render(
            request,
            "my_profile.html",
            {"modules": modules, "displayed_module": displayed_module},
        )
    else:

        modules = []
        all_modules = Module.objects.all()
        for staff_modules in all_modules:

            if request.user == staff_modules.staff.user:
                modules.append(staff_modules.name)

        return render(request, "my_profile.html", {"modules": modules})


def password_reset_request(request):
    """
    Function recives post request for an email string.
    The users email is checked against the users emails for validation.
    If correct, the email will be sent to the correct email address.
    The content sent contains a valid token link
    for the user to click in the email.
    """
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data["email"]
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.txt"
                    c = {
                        "email": user.email,
                        "domain": "127.0.0.1:8000",
                        "site_name": "Website",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(
                            subject,
                            email,
                            "lunaappliaction33@gmail.com",
                            [user.email],
                            fail_silently=False,
                        )
                    except BadHeaderError:
                        return HttpResponse("Invalid header found.")
                messages.success(
                    request,
                    "A message with reset password instructions has been sent to your inbox.",
                )
                return redirect("password_reset_done")
            messages.error(request, "An invalid email has been entered.")
    password_reset_form = PasswordResetForm()
    return render(
        request=request,
        template_name="password_reset.html",
        context={"password_reset_form": password_reset_form},
    )
