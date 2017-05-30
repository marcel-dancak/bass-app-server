from django.conf.urls import url

from basscloud.decorators import login_required, indexed_cache
from . import views


urlpatterns = [
    url(r"^profile/$", views.user_profile, name="user_profile"),
    url(r"^project/$", views.ProjectView.as_view(), name="project"),
    url(r"^projects/?$", indexed_cache(timeout=60*5)(views.ProjectsList.as_view())),
    # url(r"^projects/$", views.ProjectsList.as_view()),

    url(r"^projects/author/([0-9]+)/$",
        indexed_cache(timeout=60*5)(views.AuthorProjects.as_view()),
        name="author_projects"),
    # url(r"^projects/author/([0-9]+)/$", views.AuthorProjects.as_view()),

    # url(r"^projects/(?P<base_filter>[\w-]+)/$", views.ProjectsList.as_view()),
    url(r"^projects/((?P<base_filter>[\w-]+)/)?$", views.ProjectsList.as_view(), name="projects"),
    url(r"^bookmark/$", views.bookmark, name="bookmark"),
    url(r"^like/$", views.like, name="like"),
    url(r"^subscribe/$", views.subscribe, name="subscribe"),
    url(r"^login/$", views.client_login, name="login"),
    url(r"^logout/$", views.client_logout, name="logout")
]