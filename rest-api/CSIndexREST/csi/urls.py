from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from rest_api import views

router = DefaultRouter()
router.register(r'areas', views.AreaViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
