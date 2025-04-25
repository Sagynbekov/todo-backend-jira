# backend/api/views.py
from rest_framework import generics
from .models import Project, Column
from .serializers import ProjectSerializer, ColumnSerializer

class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    
    def get_queryset(self):
        # Get user_id from query parameters
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Project.objects.filter(user_id=user_id)
        return Project.objects.none()  # Return empty if no user_id
    
    def perform_create(self, serializer):
        # Get user_id from request data
        user_id = self.request.data.get('user_id')
        serializer.save(user_id=user_id)

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    
    def get_object(self):
        # Override get_object to handle user_id filtering properly
        queryset = self.get_queryset()
        pk = self.kwargs.get('pk')
        obj = queryset.filter(id=pk).first()
        if not obj:
            # If no object is found with user_id filter, check if it exists at all
            # This helps with debugging
            exists = Project.objects.filter(id=pk).exists()
            if exists:
                print(f"Project {pk} exists but doesn't belong to this user")
            else:
                print(f"Project {pk} doesn't exist at all")
        return obj
    
    def get_queryset(self):
        # Get user_id from both query params and request data
        user_id = None
        
        # For GET/DELETE requests, check query params first
        if self.request.method in ['GET', 'DELETE']:
            user_id = self.request.query_params.get('user_id')
        
        # For PUT/PATCH requests, check request data 
        elif self.request.method in ['PUT', 'PATCH']:
            user_id = self.request.data.get('user_id')
            # If not in data, try query params as backup
            if not user_id:
                user_id = self.request.query_params.get('user_id')
        
        if user_id:
            print(f"Filtering projects by user_id: {user_id}")
            return Project.objects.filter(user_id=user_id)
        
        print("No user_id found, returning empty queryset")
        return Project.objects.none()
    
    def perform_update(self, serializer):
        # Preserve the user_id when updating
        user_id = self.request.data.get('user_id')
        if not user_id:
            user_id = self.request.query_params.get('user_id')
        serializer.save(user_id=user_id)


class ColumnListCreateView(generics.ListCreateAPIView):
    serializer_class = ColumnSerializer
    
    def get_queryset(self):
        project_id = self.request.query_params.get('project_id')
        if project_id:
            return Column.objects.filter(project_id=project_id).order_by('order')
        return Column.objects.none()
    
    def perform_create(self, serializer):
        serializer.save()

class ColumnDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ColumnSerializer
    queryset = Column.objects.all()