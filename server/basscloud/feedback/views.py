from django.http import HttpResponse
from django.views.generic.edit import FormView

from .forms import FeedbackForm


class Feedback(FormView):
    form_class = FeedbackForm

    def form_valid(self, form):
        form.save()
        return HttpResponse("")

    def form_invalid(self, form):
        return HttpResponse(
            form.errors.as_json(),
            content_type='application/json',
            status=400
        )
