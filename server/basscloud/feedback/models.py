from django.db import models


class Feedback(models.Model):
    email = models.EmailField("email", max_length=100, blank=True)
    message = models.TextField("message")
    timestamp = models.DateTimeField("time", auto_now_add=True)

    def short_message(self, limit=120):
        if len(self.message) > limit:
            return self.message[:limit-3] + '...'
        return self.message

    def __unicode__(self):
        return self.short_message()

    class Meta:
        ordering = ["-timestamp"]