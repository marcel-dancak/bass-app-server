from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator

from registration.backends.hmac.views import RegistrationView as HmacRegistrationView

from .forms import UserRegistrationForm


class RegistrationView(HmacRegistrationView):
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


class ResetPassword(FormView):
    form_class = PasswordResetForm

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': default_token_generator,
            'email_template_name': 'accounts/password_reset_email.txt',
            'subject_template_name': 'accounts/password_reset_email_subject.txt',
            'request': self.request,
        }
        form.save(**opts)
        return HttpResponse("ko")

    def form_invalid(self, form):
        return HttpResponse(
            form.errors.as_json(),
            content_type='application/json',
            status=400
        )
