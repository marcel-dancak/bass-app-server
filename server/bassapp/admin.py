from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm

from bassapp.models import Project, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
	fieldsets = BaseUserAdmin.fieldsets[0:2] + (
        ('Profile', {'fields': ('likes', 'favourites')}),
    ) + BaseUserAdmin.fieldsets[2:]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	list_display = ('title', 'artist', 'genres', 'playing_styles', 'timestamp')
	exclude = ('id',)
	search_fields = ('title', 'artist', 'genres', 'playing_styles', 'user__username')
	list_filter = ('user__username', )
