"""bdtool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# Django Imports
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles import views
from django.conf.urls.static import static
from django.views.generic import RedirectView

admin.site.site_header = "BD Tool Administration"
admin.site.site_title = "BD Tool Backend"
admin.site.index_title = "Welcome to BD Tool Portal"

urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'^', include('project_management.urls', namespace='project_management')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', views.serve),
        url(r'^favicon\.ico$',
            RedirectView.as_view(url='/static/favicon.ico')),
    ]
