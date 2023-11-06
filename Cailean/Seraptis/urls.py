from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = "Seraptis"

urlpatterns = [
    path('', views.Index.as_view())
]