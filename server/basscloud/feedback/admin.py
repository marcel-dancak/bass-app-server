from django.contrib import admin

from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('email', 'timestamp', 'short_message')
    search_fields = ('email', 'message')
    list_filter = ('timestamp', )

    def short_message(self, obj):
        return obj.short_message(255)
    short_message.short_description = 'message'