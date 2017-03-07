import json

from lzstring import LZString
from django.conf import settings
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.gzip import gzip_page
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core import serializers

from bassapp import forms
from bassapp.models import Project
from bassapp.admin import ProjectAdmin


from django.contrib import admin
# admin = ProjectAdmin(Project, admin.site)
admin = admin.site._registry[Project]


def get_user_profile(user):
    return {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'favourites': user.favourites,
        'likes': user.likes,
        'subscribers': list(user.subscribers.values_list('pk', flat=True))
    }

@csrf_exempt
def client_login(request):
    if request.method == 'POST':
        context_type = request.META['CONTENT_TYPE']
        if context_type.startswith('application/json'):
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.POST
        form = forms.LoginForm(data)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user:
                try:
                    login(request, user)
                except Exception as e:
                    print (e)
                return JsonResponse(get_user_profile(user))
    logout(request)
    return HttpResponse("Login Required", status=401)


def client_logout(request):
    logout(request)
    return HttpResponse(" ", status=200)


@login_required
def user_profile(request):
    pass


@login_required
def projects(request):
    queryset = Project.objects.all()
    if 'q' in request.GET:
        queryset = admin.get_search_results(request, queryset, request.GET['q'])[0]

    if 'filter' in request.GET:
        f = request.GET['filter']
        if f == 'favourite':
            queryset = queryset.filter(pk__in=request.user.favourites)

    projects = []
    for project in queryset:
        projects.append({
            'id': project.pk,
            'title': project.title,
            'artist': project.artist,
            'youtube_link': project.youtube_link,
            'author': {
                'id': project.user.pk,
                'name': project.user.username,
            },
            'playing_styles': project.playing_styles,
            'genres': project.genres,
            'tags': project.tags,
            'likes': project.likes
        })
    return JsonResponse(projects, safe=False)


@csrf_exempt
@gzip_page
def project(request):
    if request.method == "POST":
        # print (request.body)
        # print  (json.loads(LZString.decompressFromUTF16(request.body.decode('utf-8'))))
        # data = json.loads(LZString.decompress(request.read()))
        print (request.body)
        data = json.loads(request.body.decode('utf-8'))
        # print (data)
        # data = json.loads(LZString.decompressFromBase64(request.body))
        # data = json.loads(LZString.decompressFromUTF16(request.body.decode('utf-8')))

        data['genres'] = ','.join(data['genres'])
        data['playing_styles'] = ','.join(data['playing_styles'])
        
        p = LZString.decompressFromBase64(data['data'])
        # print (p)
        
        form = forms.ProjectDataForm(data)
        if form.is_valid():
            # print form.cleaned_data
            project = form.save()
            return HttpResponse(project.id)
        else:
            print (form.errors)
    else:
        form = forms.GetProjectForm(request.GET)
        if form.is_valid():
            project = form.cleaned_data["id"]
            data = project.data
            # data = LZString.decompressFromBase64(project.data)
            response = HttpResponse(data, content_type='application/json')
            # response['Content-Disposition'] = 'attachment; filename={0}.json'.format(project.id)
            return response
    raise Http404


@csrf_exempt
def star(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        form = forms.ProjectVoteForm(data)
        if form.is_valid():
            project = form.cleaned_data['project']
            value = form.cleaned_data['value']

            if value and project.pk not in request.user.favourites:
                request.user.favourites.append(project.pk)
            elif not value:
                print('remove', project.pk)
                request.user.favourites.remove(project.pk)
            # request.user.favourites = []
            request.user.save()
            print(request.user.favourites)
            return HttpResponse("ok")
        else:
            print(form.errors)

    raise Http404

@csrf_exempt
def like(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        form = forms.ProjectVoteForm(data)
        if form.is_valid():
            project = form.cleaned_data['project']
            value = form.cleaned_data['value']

            if value and project.pk not in request.user.likes:
                request.user.likes.append(project.pk)
                project.likes += 1
            elif not value:
                request.user.likes.remove(project.pk)
                project.likes -= 1
            request.user.save()
            project.save()
            return HttpResponse("ok")
        else:
            print(form.errors)

    raise Http404


@csrf_exempt
def subscribe(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        form = forms.SubscribeForm(data)
        if form.is_valid():
            author = form.cleaned_data['author']
            value = form.cleaned_data['value']
            print(author, value)
    return HttpResponse("ok")



@csrf_exempt
def drawing(request):
    if request.method == "POST":
        form = forms.DrawingRecordForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("")
    else:
        form = forms.DrawingHistoryForm(request.GET)
        if form.is_valid():
            user = form.cleaned_data["USER"]
            project = form.cleaned_data["PROJECT"]
            start = form.cleaned_data["START"] or 0
            limit = form.cleaned_data["LIMIT"] or 20
            page = int(start/limit)+1
            if project:
                query = Drawing.objects.filter(user=user, project=project)
            else:
                query = Drawing.objects.filter(user=user)
            paginator = Paginator(query , limit)
            try:
                drawings = paginator.page(page)
            except EmptyPage:
                page = paginator.num_pages
                drawings = paginator.page(page)
            drawings_data = []
            for drawing in drawings:
                drawings_data .append({
                    'title': drawing.title,
                    'project': drawing.project,
                    'time': int(drawing.timestamp.strftime("%s")), #print time.mktime(drawing.timestamp.timetuple())
                    'drawing': drawing.ball_id,
                    'permalink': drawing.permalink,
                    'statistics': drawing.statistics
                })
            data = {
                'drawings': drawings_data,
                'count': paginator.count,
            }
            return HttpResponse(json.dumps(data), content_type='application/json')
    raise Http404
