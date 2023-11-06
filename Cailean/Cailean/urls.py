from django.contrib import admin
from django.urls import include,path
from django.contrib.auth import views as auth_views
from Irori.views import Index
#from django.templatetags.static import static # Not from django.conf.urls.static 
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('Irori/', include('Irori.urls')),
    path('favicon.ico', RedirectView.as_view(url="/media/favicon.ico")),
    #path('Seraptis/', include('Seraptis.urls')),
    path('', Index.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
