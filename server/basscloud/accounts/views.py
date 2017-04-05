from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.conf import settings
from registration.backends.hmac.views import RegistrationView as HmacRegistrationView

from .forms import UserRegistrationForm


class RegistrationView(HmacRegistrationView):
    form_class = UserRegistrationForm
    email_body_template_html = 'registration/activation_email.html'

    def form_valid(self, form):
        new_user = self.register(form)
        return HttpResponse("ok")

    def form_invalid(self, form):
        return HttpResponse(
            form.errors.as_json(),
            content_type='application/json',
            status=409
        )

    def send_activation_email(self, user):
        """
        Send the activation email. The activation key is simply the
        username, signed using TimestampSigner.

        """
        activation_key = self.get_activation_key(user)
        context = self.get_email_context(activation_key)
        context.update({
            'user': user
        })

        subject = render_to_string(self.email_subject_template, context)
        # Force subject to a single line to avoid header-injection issues.
        subject = ''.join(subject.splitlines())
        message = render_to_string(self.email_body_template, context)
        html_message = render_to_string(self.email_body_template_html, context)
        user.email_user(subject, message, settings.DEFAULT_FROM_EMAIL, html_message=html_message)


class ResetPassword(FormView):
    form_class = PasswordResetForm

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': default_token_generator,
            'email_template_name': 'accounts/password_reset_email.txt',
            'html_email_template_name': 'accounts/password_reset_email.html',
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
