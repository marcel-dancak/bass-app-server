from django.conf import settings
from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    url(r'', include('basscloud.catalog.urls', namespace='catalog')),
    url(r'', include('basscloud.app.urls', namespace='app')),
    url(r'^accounts/', include('basscloud.accounts.urls')),
    url(r'^admin/', include(admin.site.urls))
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
