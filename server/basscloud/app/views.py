
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from basscloud.catalog.models import Project
from basscloud.libs.lzstring import LZString



def app(request):
    return render(request, "app/index.html")


def app_data(request, id, *args):
    project = get_object_or_404(Project, pk=id)
    data = LZString.decompressFromBase64(project.data)
    return HttpResponse(data, content_type='application/json')
