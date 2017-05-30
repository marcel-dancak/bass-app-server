from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^projects/?$", views.projects_list, name="projects_list"),
    url(r"^project/(\w+)/?$", views.project, name="project")
]
