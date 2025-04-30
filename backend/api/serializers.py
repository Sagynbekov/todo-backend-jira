# backend/api/serializers.py

from rest_framework import serializers
from .models import Project, Column, Task, FirebaseUser

class FirebaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirebaseUser
        fields = ['firebase_user_id', 'email', 'profile_photo']

class ProjectSerializer(serializers.ModelSerializer):
    members = serializers.SlugRelatedField(
        many=True,
        slug_field='email',
        queryset=FirebaseUser.objects.all(),
        required=False
    )

    class Meta:
        model = Project
        fields = ['id', 'name', 'user_id', 'members']
        read_only_fields = ['id']

class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = ['id', 'name', 'project', 'order']

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'column', 'order', 'created_at', 'updated_at', 'creator_id', 'creator_email']
