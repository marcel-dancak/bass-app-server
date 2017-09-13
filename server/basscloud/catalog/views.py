import json
import logging

# from lzstring import LZString
from django.conf import settings
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden, Http404
from django.views import View
from django.views.decorators.gzip import gzip_page
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.cache import cache

# TODO move to accounts app
from basscloud.decorators import login_required
from basscloud.libs.lzstring import LZString
from . import forms
from .models import Project

from django.contrib import admin
admin = admin.site._registry[Project]
# from basscloud.admin import ProjectAdmin
# admin = ProjectAdmin(Project, admin.site)


logger = logging.getLogger(__name__)


@ensure_csrf_cookie
def catalog(request):
    data = {}

    structured_meta = cache.get('structured_meta:index')
    if not structured_meta:
        structured_meta = render_to_string(
            'catalog/json_meta',
            {'projects': Project.objects.filter(public=True)[:50]}
        )
        cache.set('structured_meta:index', structured_meta, 60*60)
    data['structured_meta'] = structured_meta

    if request.user.is_authenticated():
        data['userProfile'] = json.dumps(get_user_profile(request.user))
    return render(request, "catalog/index.html", data)


def get_user_profile(user):
    return {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'avatar': user.avatar.url if user.avatar else '',
        'bookmarks': user.bookmarks,
        'likes': user.likes,
        'links': user.links,
        'subscribed': list(user.subscribed.values_list('pk', flat=True)),
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

        form = AuthenticationForm(data=data)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return JsonResponse(get_user_profile(user))

        return HttpResponse(
            form.errors.as_json(),
            content_type='application/json',
            status=403
        )
    logout(request)
    return HttpResponse("Login Required", status=401)


def client_logout(request):
    logout(request)
    return HttpResponse(" ", status=200)


@ensure_csrf_cookie # just for development!
def user_profile(request):
    if request.user and request.user.is_authenticated():

        if request.method == 'POST':
            # data = json.loads(request.body.decode('utf-8'))
            form = forms.UserProfileForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
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
            } if project.user else {},
            'playing_styles': project.playing_styles,
            'genres': project.genres,
            'tracks': project.tracks,
            'tags': project.tags,
            'likes': project.likes,
            'level': project.level,
            'category': project.category,
            'created': project.created,
            'modified': project.modified,
            'options': project.options
        })
    return projects


class ProjectsFilterMixin(object):
    levels = {
        'A': {'level__lte': 1},
        'B': {'level__lte': 2},
        'C': {'level__range': (1,4)},
        'D': {'level__range': (2,5)},
        'E': {'level__range': (4,6)}
    }
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

        if 'level' in request.GET:
            queryset = queryset.filter(**self.levels[request.GET['level']])

        if 'sort' in request.GET:
            queryset = queryset.order_by(request.GET['sort'])

        return queryset


from django.views.generic.list import MultipleObjectMixin

class ProjectsList(ProjectsFilterMixin, MultipleObjectMixin, View):

    @method_decorator(gzip_page)
    def get(self, request, base_filter=None):
        # or select_related
        # queryset = Project.objects.all()
        queryset = Project.objects.defer('data').prefetch_related('user')

        if base_filter and request.user.is_authenticated():
            if base_filter == 'bookmarked' :
                queryset = queryset.filter(pk__in=request.user.bookmarks)

            if base_filter == 'subscribed':
                queryset = queryset.filter(user__in=request.user.subscribed.all())

            if base_filter == 'created':
                queryset = queryset.filter(user=request.user)

        queryset = self.filter(queryset, request)

        paginator, page, queryset, has_other_pages = self.paginate_queryset(queryset, 25)
        return JsonResponse({
            'projects': get_projects_data(queryset),
            'paginator': {
                'has_other_pages': has_other_pages,
                'page': page.number,
                'pages': paginator.num_pages,
                # 'total': queryset.count()
            }
        })
        return JsonResponse(get_projects_data(queryset), safe=False)


class AuthorProjects(ProjectsFilterMixin, View):

    @method_decorator(gzip_page)
    def get(self, request, author):
        author = get_object_or_404(get_user_model(), id=author)
        queryset = Project.objects.defer('data').filter(user=author)
        queryset = self.filter(queryset, request)

        # use already fetched author model to avoid additional db queries
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
                'subscribers_count': author.subscribers.count(),
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
        initial = {'user': request.user.pk}

        # data = json.loads(LZString.decompressFromBase64(request.body))
        # data = json.loads(LZString.decompressFromUTF16(request.body.decode('utf-8')))
        instance = None
        if 'id' in data:
            instance = get_object_or_404(Project, pk=data['id'])
            if instance.user != request.user and not request.user.is_superuser:
                return HttpResponseForbidden()

        form = forms.ProjectDataForm(data, instance=instance, initial=initial)
        if form.is_valid():
            # print (form.cleaned_data)
            # p = LZString.decompressFromBase64(data['data'])
            # print (p)
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
def bookmark(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        form = forms.ProjectVoteForm(data)
        if form.is_valid():
            project = form.cleaned_data['project']
            value = form.cleaned_data['value']

            if value and project.pk not in request.user.bookmarks:
                request.user.bookmarks.append(project.pk)
            elif not value:
                request.user.bookmarks.remove(project.pk)
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
                request.user.subscribed.add(author)
            else:
                request.user.subscribed.remove(author)
    return HttpResponse("ok")
