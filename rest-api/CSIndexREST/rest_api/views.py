from django.db.models import Count, FloatField, Min, Q, Value
from django.utils.six.moves.urllib import parse as urlparse
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.schemas import AutoSchema
import coreapi

from .models import Area, Conference, Department, Researcher, Paper
from .serializers import AreaSerializer, ConferenceSerializer, DepartmentSerializer, ResearcherSerializer, \
    PaperSerializer


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
    queryset = Area.objects.annotate(papers_count=Count('conference__paper__url', distinct=True))
    serializer_class = AreaSerializer


class ConferenceFilter(filters.FilterSet):
    area = filters.CharFilter(name='area__name', label='Area name', distinct=True)

    class Meta:
        model = Conference
        fields = ['area', 'name']


class ConferenceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ConferenceSerializer
    queryset = Conference.objects.annotate(papers_count=Count('paper__url', distinct=True)).order_by('area__name',
                                                                                                     '-papers_count',
                                                                                                     'name')
    filter_class = ConferenceFilter
    schema = FilterListOnlySchema()


class DepartmentFilter(filters.FilterSet):
    area = filters.CharFilter(name='area', label='Area name', method='filter_area')

    def filter_area(self, queryset, name, value):
        query = Department.objects.filter(departmentscore__area__name=value)
        query = query.annotate(score_value=Min('departmentscore__value'))
        query = query.annotate(researchers_count=Count('researcher__name', distinct=True,
                                                       filter=Q(researcher__paper__conference__area__name=value)))
        query = query.order_by('-score_value', 'name')
        return query

    class Meta:
        model = Department
        fields = ['area', 'name']


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Department.objects.annotate(researchers_count=Count('researcher__name', distinct=True),
                                           score_value=Value(-1.0,
                                                             output_field=FloatField())).order_by('-researchers_count',
                                                                                                  'name')
    serializer_class = DepartmentSerializer
    filter_class = DepartmentFilter


class ResearcherFilter(filters.FilterSet):
    area = filters.CharFilter(name='paper__conference__area__name', label='Area name', distinct=True)
    department = filters.CharFilter(name='department__name', label='Department name', distinct=True)

    class Meta:
        model = Researcher
        fields = ['area', 'department']


class ResearcherViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Researcher.objects.all()
    serializer_class = ResearcherSerializer
    filter_class = ResearcherFilter
    schema = FilterListOnlySchema()


class PaperFilter(filters.FilterSet):
    area = filters.CharFilter(name='conference__area__name', label='Area name', distinct=True)
    conference = filters.CharFilter(name='conference__name', label='Conference name', distinct=True)
    department = filters.CharFilter(name='researchers__department__name', label='Department name', distinct=True)
    researchers = filters.CharFilter(name='researchers__name', label='Researcher name', distinct=True)

    class Meta:
        model = Paper
        fields = ['area', 'conference', 'department', 'researchers', 'year']


class PaperViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Paper.objects.all()
    serializer_class = PaperSerializer
    filter_class = PaperFilter
    schema = FilterListOnlySchema()
