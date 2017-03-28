from django.http import HttpResponse

from registration.backends.hmac.views import RegistrationView
from .forms import UserRegistrationForm


class SpaRegistrationView(RegistrationView):
    form_class = UserRegistrationForm

    def form_valid(self, form):
        new_user = self.register(form)
        return HttpResponse("ok")

    def form_invalid(self, form):
        return HttpResponse(
            form.errors.as_json(),
            content_type='application/json',
            status=409
        )
