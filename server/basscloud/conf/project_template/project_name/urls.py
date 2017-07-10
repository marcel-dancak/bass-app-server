from django.conf import settings
from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.contrib import admin

from basscloud.catalog import views


urlpatterns = [
    url(r'', include('basscloud.catalog.urls', namespace='catalog')),
    url(r'api/', include('basscloud.catalog.api', namespace='api')),
    url(r'', include('basscloud.app.urls', namespace='app')),
    url(r'api/', include('basscloud.feedback.api', namespace='api')),
    url(r'^accounts/', include('basscloud.accounts.urls')),
    url(r'^api/accounts/', include('basscloud.accounts.api', namespace='api')),
    url(r'^admin/', include(admin.site.urls)),

    url(r'seo/', include('basscloud.seo.urls', namespace='seo'))
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Catch all unknown urls as root path (SPA)
urlpatterns += [url(r'^.*', views.catalog)]