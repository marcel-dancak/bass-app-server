from django.conf.urls import url, include
from django.contrib.auth.views import password_reset, password_reset_confirm, password_reset_complete

from .views import RegistrationView, ResetPassword


urlpatterns = [
    url(r'^register/$',
        RegistrationView.as_view(),
        name='registration_register'
    ),
    url(r'^password_reset/$',
        ResetPassword.as_view(),
        name='password_reset'
    ),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm,
        {'template_name': 'accounts/password_reset_confirm.html'},
        name='password_reset_confirm'
    ),
    url(r'^reset/done/$',
        password_reset_complete,
        {'template_name': 'accounts/password_reset_complete.html'},
        name='password_reset_complete'
    ),
    url(r'', include('registration.backends.hmac.urls')),
]
