from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http import Http404

from basscloud.catalog.models import Project


def project(request, id):
    project = get_object_or_404(Project, pk=id)
    return render(
        request,
        "seo/project.html",
        {'project': project}
    )


def projects_list(request):
    if 'artists' in request.GET:
        queryset = Project.objects.filter(artist=request.GET['artists'])
    else:
        queryset = Project.objects.all()

    return render(
        request,
        "seo/projects_list.html",
        {'projects': queryset}
    )