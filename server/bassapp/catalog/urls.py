from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^$", views.catalog, name="catalog"),
    url(r"^profile/$", views.user_profile, name="user_profile"),
    url(r"^project/$", views.ProjectView.as_view(), name="project"),
    url(r"^projects/author/([0-9]+)/$", views.AuthorProjects.as_view(), name="user_projects"),
    url(r"^projects/((?P<base_filter>[\w-]+)/)?$", views.ProjectsList.as_view(), name="projects"),
    url(r"^star/$", views.star, name="star"),
    url(r"^like/$", views.like, name="like"),
    url(r"^subscribe/$", views.subscribe, name="subscribe"),
    url(r"^login/$", views.client_login, name="login"),
    url(r"^logout/$", views.client_logout, name="logout")
]
