from django.conf.urls import url, include

from .views import SpaRegistrationView


urlpatterns = [
    url(r'register/$',
        SpaRegistrationView.as_view(),
        name='registration_register',
    ),
    url(r'', include('registration.backends.hmac.urls')),
]
