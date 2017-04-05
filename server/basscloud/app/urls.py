from django.conf.urls import url

from . import views


urlpatterns = [
    url(r"^app$", views.app, name="app"),
    url(r"^app/(\w+)(.json/)?$", views.app_data, name="app_data")
]
