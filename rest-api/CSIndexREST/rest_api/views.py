from rest_framework import viewsets

from .models import Area, Conference
from .serializers import AreaSerializer, ConferenceSerializer


class AreaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


class ConferenceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ConferenceSerializer
    queryset = Conference.objects.all()

    def get_queryset(self):
        queryset = Conference.objects.all()
        area_name = self.request.query_params.get('area', None)
        if area_name:
            queryset = queryset.filter(area__name=area_name)
        return queryset
