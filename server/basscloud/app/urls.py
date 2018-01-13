from django.conf.urls import url

from . import views
from basscloud.decorators import view_cache


urlpatterns = [
    url(r"^app$", views.app, name="app"),
    url(r"^app/(\w+-v\d+)$", views.forked_project_data, name="forked_project_data"),
    # url(r"^app/(\w+)-v(\d+)$", view_cache(timeout=60*5)(views.forked_project_data), name="forked_project_data"),
    url(r"^app/(\w+)(.json/)?$", view_cache(timeout=60*5)(views.app_data), name="project_data"),
    url(r"^api/online_stream/$", views.extract_streams)
]
