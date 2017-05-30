from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^register/$',
        views.RegistrationView.as_view(),
        name='registration_register'
    ),
    url(r'^password_reset/$',
        views.ResetPassword.as_view(),
        name='password_reset'
    )
]