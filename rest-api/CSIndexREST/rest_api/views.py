from django.utils.six.moves.urllib import parse as urlparse
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.schemas import AutoSchema
import coreapi

from .models import Area, Conference, Department
from .serializers import AreaSerializer, ConferenceSerializer, DepartmentSerializer


class FilterListOnlySchema(AutoSchema):
    def get_link(self, path, method, base_url):
        fields = self.get_path_fields(path, method)
        fields += self.get_serializer_fields(path, method)
        fields += self.get_pagination_fields(path, method)
        if self.view.action in ['list']:
            fields += self.get_filter_fields(path, method)

        manual_fields = self.get_manual_fields(path, method)
        fields = self.update_fields(fields, manual_fields)

        if fields and any([field.location in ('form', 'body') for field in fields]):
            encoding = self.get_encoding(path, method)
        else:
            encoding = None

        description = self.get_description(path, method)

        if base_url and path.startswith('/'):
            path = path[1:]

        return coreapi.Link(
            url=urlparse.urljoin(base_url, path),
            action=method.lower(),
            encoding=encoding,
            fields=fields,
            description=description
        )


class AreaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


class ConferenceFilter(filters.FilterSet):
    area = filters.CharFilter(name='area__name', label='Area name')

    class Meta:
        model = Conference
        fields = ['area']


class ConferenceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ConferenceSerializer
    queryset = Conference.objects.all()
    filter_class = ConferenceFilter
    schema = FilterListOnlySchema()


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer