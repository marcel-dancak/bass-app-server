from django.conf import settings
from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    url(r'', include('bassapp.catalog.urls', namespace='catalog')),
    url(r'', include('bassapp.app.urls', namespace='app')),
    url(r'^admin/', include(admin.site.urls))
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
