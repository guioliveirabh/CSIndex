from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view

from rest_api import views

router = DefaultRouter()
router.register(r'areas', views.AreaViewSet)
router.register(r'conferences', views.ConferenceViewSet)

title = 'CSIndex'

urlpatterns = [
                  url(r'^', include(router.urls)),
                  url(r'^docs/', include_docs_urls(title=title)),
                  url(r'^schema/$', get_schema_view(title=title))
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
