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
    creator_email = serializers.EmailField(source='creator.email', read_only=True)
    completed_by_email = serializers.EmailField(source='completed_by.email', read_only=True, allow_null=True)
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'column', 'order', 'created_at', 'updated_at', 'creator', 'creator_email', 'completed', 'completed_by', 'completed_by_email', 'deadline']
        read_only_fields = ['creator_email', 'completed_by_email']
