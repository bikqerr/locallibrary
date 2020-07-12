from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    # Use include to add paths from the catalog application
    path('catalog/', include('catalog.urls')),
    # Add URL maps to redirect the base URL to our application
    path('', RedirectView.as_view(url='catalog/', permanent=True)),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += [
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]
