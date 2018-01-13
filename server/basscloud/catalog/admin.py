from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm

from .models import Project, User, ForkedProject


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets[0:2] + (
        ('Profile', {'fields': ('likes', 'bookmarks', 'avatar')}),
    ) + BaseUserAdmin.fieldsets[2:]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'genres', 'playing_styles', 'created')
    exclude = ('id', 'likes')
    search_fields = ('title', 'artist', 'genres', 'playing_styles', 'user__username')
    list_filter = ('user', )


@admin.register(ForkedProject)
class ForkedProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'tag', 'original_author', 'user', 'created', 'modified')
    readonly_fields = ('project_id', 'tag', 'user', 'created', 'modified')
    fields = ('project_id', 'tag', 'user', 'created', 'modified', 'data')

    def project_id(self, obj):
        return obj.project.id

    def title(self, obj):
        return obj.project.title

    def artist(self, obj):
        return obj.project.artist

    def original_author(self, obj):
        return obj.project.user
