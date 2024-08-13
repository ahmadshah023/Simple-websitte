from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include, re_path
from . import views


urlpatterns = [
                  path('', views.project, name='project'),
                  path('da/', views.data_analysis, name='data_analysis'),
                  path('success/', views.success, name='success'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
