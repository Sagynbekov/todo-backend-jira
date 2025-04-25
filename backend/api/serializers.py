# backend/api/serializers.py

from rest_framework import serializers
from .models import Project, Column


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'user_id']
        read_only_fields = ['id']


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['id', 'name', 'project', 'order']