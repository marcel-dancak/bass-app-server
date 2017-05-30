from django.shortcuts import render
from django.shortcuts import get_object_or_404

from basscloud.catalog.models import Project


def project(request, id):
    project = get_object_or_404(Project, pk=id)
    return render(
        request,
        "seo/project.html",
        {'project': project}
    )


def projects_list(request):
    # project = get_object_or_404(Project, pk=id)
    return render(
        request,
        "seo/projects_list.html",
        {'projects': Project.objects.all()}
    )