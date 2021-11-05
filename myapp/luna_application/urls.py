from django.urls import path
from .views import (
    post_detail_view,
    post_create_view,
    post_update_view,
    post_delete_view,
    network_create_view,
    module_post_detail_view,
    module_post_create_view,
    module_post_update_view,
    module_post_delete_view,
)
from . import views

urlpatterns = [
    path("", views.start_page, name="luna_application-start_page"),
    path("home/", views.home_page, name="luna_application-home_page"),
    path(
        "wellbeing_tasks/",
        views.wellbeing_tasks,
        name="luna_application-wellbeing_tasks",
    ),
    path("leaderboards/", views.leaderboards,
         name="luna_application-leaderboards"),
    path(
        "student_networks/",
        views.student_networks,
        name="luna_application-student_networks",
    ),
    path("student_networks/new/",
         network_create_view.as_view(), name="network_create"),
    path(
        "network_display/",
        views.display_network,
        name="luna_application-network_display",
    ),
    path(
        "network_display/post/<int:pk>/", post_detail_view.as_view(), name="post_detail"
    ),
    path("network_display/post/new/",
         post_create_view.as_view(), name="post_create"),
    path(
        "network_display/post/<int:pk>/update",
        post_update_view.as_view(),
        name="post_update",
    ),
    path(
        "network_display/post/<int:pk>/delete",
        post_delete_view.as_view(),
        name="post_delete",
    ),
    path(
        "network_post_like/<int:pk>", views.network_post_like, name="networkpost_like"
    ),
    path(
        "network_post_report/<int:pk>",
        views.network_post_report,
        name="networkpost_report",
    ),
    path(
        "network_post_comment/<int:pk>",
        views.network_post_comment,
        name="networkpost_comment",
    ),
    path(
        "academic_network/",
        views.academic_network,
        name="luna_application-academic_network",
    ),
    path("assign_tasks/", views.assign_tasks,
         name="luna_application-assign_tasks"),
    path(
        "module_display/", views.module_display, name="luna_application-module_display"
    ),
    path(
        "module_display/post/<int:pk>/",
        module_post_detail_view.as_view(),
        name="module_post_detail",
    ),
    path(
        "module_display/post/new/",
        module_post_create_view.as_view(),
        name="module_post_create",
    ),
    path(
        "module_display/post/<int:pk>/update",
        module_post_update_view.as_view(),
        name="module_post_update",
    ),
    path(
        "module_display/post/<int:pk>/delete",
        module_post_delete_view.as_view(),
        name="module_post_delete",
    ),
    path("module_post_like/<int:pk>",
         views.module_post_like, name="modulepost_like"),
    path(
        "module_post_report/<int:pk>",
        views.module_post_report,
        name="modulepost_report",
    ),
    path(
        "module_post_comment/<int:pk>",
        views.module_post_comment,
        name="modulepost_comment",
    ),
    path("my_profile/", views.my_profile, name="luna_application-my_profile"),
    path("user_set_tasks/", views.get_user_task),
    path("update_daily_tasks/", views.update_daily_tasks),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path("hub/", views.guest_login, name="luna_application-the_hub"),
]
