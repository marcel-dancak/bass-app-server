from django.conf.urls import url

from bassapp import views


urlpatterns = [
    url(r"^$", views.catalog, name="catalog"),
    url(r"^app/$", views.app, name="app"),
    url(r"^app/(\w+)/(.json/)?$", views.app_data, name="app_data"),
    url(r"^profile/$", views.user_profile, name="user_profile"),
    url(r"^project/$", views.project, name="project"),
    url(r"^projects/author/([0-9]+)/$", views.user_projects, name="user_projects"),
    url(r"^projects/((?P<filter>[\w-]+)/)?$", views.projects, name="projects"),
    url(r"^star/$", views.star, name="star"),
    url(r"^like/$", views.like, name="like"),
    url(r"^subscribe/$", views.subscribe, name="subscribe"),
    url(r"^login/$", views.client_login, name="login"),
    url(r"^logout/$", views.client_logout, name="logout")
]
