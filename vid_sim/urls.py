# myproject/urls.py

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')), 
    path('', lambda request: HttpResponseRedirect('/upload/')),  # Redirect to upload page

]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
