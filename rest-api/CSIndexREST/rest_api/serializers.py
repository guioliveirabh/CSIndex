from rest_framework import serializers

from .models import Area, Conference, Department, Researcher, Paper


class AreaSerializer(serializers.ModelSerializer):
    papers_count = serializers.IntegerField()

    class Meta:
        model = Area
        fields = ('id', 'name', 'label', 'papers_count')


class ConferenceSerializer(serializers.ModelSerializer):
    area = serializers.StringRelatedField(many=False)
    papers_count = serializers.IntegerField()

    class Meta:
        model = Conference
        fields = ('id', 'area', 'name', 'papers_count')


class DepartmentSerializer(serializers.ModelSerializer):
    researchers_count = serializers.IntegerField()
    score_value = serializers.FloatField()

    class Meta:
        model = Department
        fields = ('id', 'name', 'researchers_count', 'score_value')


class ResearcherSerializer(serializers.ModelSerializer):
    department = serializers.StringRelatedField(many=False)

    class Meta:
        model = Researcher
        fields = ('id', 'name', 'department', 'pid')


class PaperSerializer(serializers.ModelSerializer):
    conference = serializers.StringRelatedField(many=False)
    researchers = serializers.StringRelatedField(many=True)

    def to_representation(self, obj):
        representation = super().to_representation(obj)
        representation['researchers'] = '; '.join(representation['researchers'])
        return representation

    class Meta:
        model = Paper
        fields = ('id', 'title', 'conference', 'researchers', 'year', 'authors', 'url')
