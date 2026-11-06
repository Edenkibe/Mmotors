
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.core.urls')),
    path('',include('apps.accounts.urls', namespace='accounts')),
    path('',include('apps.voiture.urls', namespace='voiture')),
    path('',include('apps.promotion.urls', namespace='promotion')),
    path('',include('apps.dossiers.urls', namespace='dossiers')),
    path('',include('apps.contact.urls', namespace='contact')),
    path('',include('apps.location.urls', namespace='location')),
    path('',include('apps.integration.urls', namespace='integration'))
       
]
urlpatterns += [
    re_path(
        r'^voitures/(?P<path>.*)$',
        serve,
        {'document_root': settings.MEDIA_ROOT}
    ),
]

#to read all image in the db:
if settings.DEBUG:
    urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)