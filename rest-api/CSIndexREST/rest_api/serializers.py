from rest_framework import serializers

from .models import Area, Conference, Department, Researcher


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ('id', 'name', 'label')


class ConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conference
        fields = ('id', 'area', 'name')


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'name')


class ResearcherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Researcher
        fields = ('id', 'name', 'department', 'pid')
