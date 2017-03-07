from django.conf.urls import url

from bassapp import views


urlpatterns = [
    url(r"^project/$", views.project, name="project"),
    url(r"^projects/$", views.projects, name="projects"),
    url(r"^star/$", views.star, name="star"),
    url(r"^like/$", views.like, name="like"),
    url(r"^subscribe/$", views.subscribe, name="subscribe"),
    url(r"^login/$", views.client_login, name="login"),
    url(r"^logout/$", views.client_logout, name="logout")
]
