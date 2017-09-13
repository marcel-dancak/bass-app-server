from django.conf.urls import url

from . import views


urlpatterns = [
    # url(r"^upload/$", views.upload, name="upload"),
    url(r"^list/$", views.get_files, name="list"),
    url(r"^get/$", views.get, name="get"),
    url(r"^info/$", views.info, name="info")
]
