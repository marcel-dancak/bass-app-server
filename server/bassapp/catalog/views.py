import json
import logging

# from lzstring import LZString
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views import View
from django.views.decorators.gzip import gzip_page
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from django.core.paginator import Paginator, EmptyPage
# from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Q

from bassapp.decorators import login_required
from bassapp.libs.lzstring import LZString
from . import forms
from .models import Project

from django.contrib import admin
admin = admin.site._registry[Project]
# from bassapp.admin import ProjectAdmin
# admin = ProjectAdmin(Project, admin.site)


logger = logging.getLogger(__name__)

@ensure_csrf_cookie
def catalog(request):
    logger.info('Catalog App touched!')
    return render(request, "catalog/index.html")


def get_user_profile(user):
    return {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'avatar': user.avatar.url if user.avatar else '',
        'favourites': user.favourites,
        'likes': user.likes,
        'links': user.links,
        'subscribers': list(user.subscribers.values_list('pk', flat=True)),
        'projectsCount': Project.objects.filter(user=user).count()
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


def user_profile(request):
    if request.user and request.user.is_authenticated():

        if request.method == 'POST':
            # data = json.loads(request.body.decode('utf-8'))
            form = forms.UserProfileForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                print (form.cleaned_data)
                user = form.save()
                return JsonResponse(get_user_profile(user))
            else:
                print(form.errors)
                raise Http404
        else:
            return JsonResponse(get_user_profile(request.user))

    return HttpResponse(status=401)


def get_projects_data(queryset):
    projects = []
    for project in queryset:
        projects.append({
            'id': project.pk,
            'title': project.title,
            'artist': project.artist,
            'description': project.description,
            'video_link': project.video_link,
            'author': {
                'id': project.user.pk,
                'name': project.user.username,
                'avatar': project.user.avatar.url if project.user.avatar else ''
            },
            'playing_styles': project.playing_styles,
            'genres': project.genres,
            'tracks': project.tracks,
            'tags': project.tags,
            'likes': project.likes,
            'level': project.level,
            'category': project.category,
            'created': project.created,
            'modified': project.modified
        })
    return projects


class ProjectsFilterMixin(object):
    def filter(self, queryset, request):
        if 'q' in request.GET:
            queryset = admin.get_search_results(request, queryset, request.GET['q'])[0]

        if 'genres' in request.GET:
            queryset = queryset.filter(genres__overlap=request.GET['genres'].split(','))

        if 'styles' in request.GET:
            queryset = queryset.filter(playing_styles__overlap=request.GET['styles'].split(','))

        if 'artists' in request.GET:
            artists = request.GET['artists'].split(',')
            q = Q(artist__icontains=artists[0])
            for artist in artists[1:]:
                q = q | Q(artist__icontains=artist)
            queryset = queryset.filter(q)

        if 'authors' in request.GET:
            authors = request.GET['authors'].split(',')
            q = Q(user__username__icontains=authors[0])
            for author in authors[1:]:
                q = q | Q(user__username__icontains=author)
            queryset = queryset.filter(q)
        return queryset


class ProjectsList(ProjectsFilterMixin, View):

    @method_decorator(gzip_page)
    def get(self, request, base_filter=None):
        # queryset = Project.objects.all()
        queryset = Project.objects.defer('data', 'data_public').prefetch_related('user')

        if base_filter == 'favourite' and request.user.is_authenticated():
            queryset = queryset.filter(pk__in=request.user.favourites)

        if base_filter == 'subscribers':
            queryset = queryset.filter(user__in=request.user.subscribers.all())

        if base_filter == 'my':
            queryset = queryset.filter(user=request.user)

        if base_filter == 'liked':
            queryset = queryset.order_by('-likes')

        queryset = self.filter(queryset, request)
        return JsonResponse(get_projects_data(queryset), safe=False)



class AuthorProjects(ProjectsFilterMixin, View):

    @method_decorator(gzip_page)
    def get(self, request, author):
        author = get_user_model().objects.get(id=author)
        queryset = Project.objects.defer('data', 'data_public').filter(user=author)
        queryset = self.filter(queryset, request)

        # user already fetched author model to avoid additional db queries
        projects = list(queryset)
        for project in projects:
            project.user = author

        projects = get_projects_data(projects)
        data = {
            'profile': {
                'id': author.id,
                'username': author.username,
                'first_name': author.first_name,
                'last_name': author.last_name,
                'date_joined': author.date_joined,
                'projects_count': len(projects),
                'avatar': author.avatar.url if author.avatar else '',
                'links': author.links
            },
            'projects': projects
        }
        return JsonResponse(data)


@method_decorator(csrf_exempt, name='dispatch')
class ProjectView(View):

    @method_decorator(login_required)
    def post(self, request):
        # print (request.body)
        # print  (json.loads(LZString.decompressFromUTF16(request.body.decode('utf-8'))))
        # data = json.loads(LZString.decompress(request.read()))
        # print (request.body)
        data = json.loads(request.body.decode('utf-8'))

        # data = json.loads(LZString.decompressFromBase64(request.body))
        # data = json.loads(LZString.decompressFromUTF16(request.body.decode('utf-8')))

        instance = None
        if 'id' in data:
            instance = get_object_or_404(Project, pk=data['id'])
            # TODO: check user permissions

        # for param in ('genres', 'playing_styles', 'tags')

        form = forms.ProjectDataForm(data, instance=instance)
        if form.is_valid():
            print (form.cleaned_data)
            # p = LZString.decompressFromBase64(data['data'])
            # print (p)
            raise Exception("Uploading not yet implemented!")
            return HttpResponse("ok")
            # project.user = self.request.user
            project = form.save()
            return HttpResponse(project.id)
        else:
            print (form.errors)
        raise Http404


    def get(self, request):
        form = forms.GetProjectForm(request.GET)
        if form.is_valid():
            project = form.cleaned_data['id']
            project_data = get_projects_data([project])[0]
            if form.cleaned_data['data']:
                # TODO: data shoud depend on authentication
                data = project.data
                # data = LZString.decompressFromBase64(project.data)
                project_data['data'] = project.data

            return JsonResponse(project_data)
        raise Http404


@login_required
def star(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        form = forms.ProjectVoteForm(data)
        if form.is_valid():
            project = form.cleaned_data['project']
            value = form.cleaned_data['value']

            if value and project.pk not in request.user.favourites:
                request.user.favourites.append(project.pk)
            elif not value:
                request.user.favourites.remove(project.pk)
            request.user.save()
            return HttpResponse("ok")
        else:
            print(form.errors)

    raise Http404

@login_required
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


@login_required
def subscribe(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        form = forms.SubscribeForm(data)
        if form.is_valid():
            author = form.cleaned_data['author']
            value = form.cleaned_data['value']
            if value:
                request.user.subscribers.add(author)
            else:
                request.user.subscribers.remove(author)
    return HttpResponse("ok")
