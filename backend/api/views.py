from rest_framework import generics
from django.db.models import Q
from rest_framework.response import Response
from .models import Project, Column, Task, FirebaseUser
from .serializers import ProjectSerializer, ColumnSerializer, TaskSerializer, FirebaseUserSerializer
from rest_framework.parsers import MultiPartParser, FormParser




class ProjectListCreateView(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Project.objects.filter(
                Q(user_id=user_id) |
                Q(members__firebase_user_id=user_id)
            ).distinct()
        return Project.objects.none()

    def perform_create(self, serializer):
        user_id = self.request.data.get('user_id')
        project = serializer.save(user_id=user_id)
        for email in self.request.data.get('members', []):
            try:
                member = FirebaseUser.objects.get(email=email)
                project.members.add(member)
            except FirebaseUser.DoesNotExist:
                pass

class ProjectDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer

    def get_queryset(self):
        user_id = None
        if self.request.method in ['GET', 'DELETE']:
            user_id = self.request.query_params.get('user_id')
        elif self.request.method in ['PUT', 'PATCH']:
            user_id = self.request.data.get('user_id') or self.request.query_params.get('user_id')

        if user_id:
            return Project.objects.filter(
                Q(user_id=user_id) |
                Q(members__firebase_user_id=user_id)
            ).distinct()
        return Project.objects.none()

    def get_object(self):
        queryset = self.get_queryset()
        pk = self.kwargs.get('pk')
        return queryset.filter(id=pk).first()

    def perform_update(self, serializer):
        project = serializer.save()
        if 'members' in self.request.data:
            project.members.clear()
            for email in self.request.data.get('members', []):
                try:
                    member = FirebaseUser.objects.get(email=email)
                    project.members.add(member)
                except FirebaseUser.DoesNotExist:
                    pass

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

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        column_id = self.request.query_params.get('column_id')
        if column_id:
            return Task.objects.filter(column_id=column_id).order_by('order')
        return Task.objects.none()
    
    def perform_create(self, serializer):
        creator_uid = self.request.data.get('creator_id')  # uid FirebaseUser.firebase_user_id
        # найдём объект FirebaseUser по uid
        try:
            user = FirebaseUser.objects.get(firebase_user_id=creator_uid)
        except FirebaseUser.DoesNotExist:
            user = None
        serializer.save(creator=user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    
    def perform_update(self, serializer):
        # Check if the task is being marked as completed
        if 'completed' in self.request.data and self.request.data['completed'] == True:
            # Get the current task object
            task = self.get_object()
            
            # Only update completed_by if the task is being newly completed
            if not task.completed:
                # Get current user
                user_id = self.request.data.get('user_id') or self.request.query_params.get('user_id')
                if user_id:
                    try:
                        user = FirebaseUser.objects.get(firebase_user_id=user_id)
                        serializer.save(completed_by=user)
                        return
                    except FirebaseUser.DoesNotExist:
                        pass
        
        # For any other updates or if user not found
        serializer.save()

class FirebaseUserListCreateView(generics.ListCreateAPIView):
    queryset = FirebaseUser.objects.all()
    serializer_class = FirebaseUserSerializer

    def get_queryset(self):
        email = self.request.query_params.get('email')
        uid   = self.request.query_params.get('firebase_user_id')
        if email:
            return FirebaseUser.objects.filter(email=email)
        if uid:
            return FirebaseUser.objects.filter(firebase_user_id=uid)
        return FirebaseUser.objects.none()

    def perform_create(self, serializer):
        uid = serializer.validated_data['firebase_user_id']
        email = serializer.validated_data['email']
        instance, _ = FirebaseUser.objects.get_or_create(
            firebase_user_id=uid,
            defaults={'email': email}
        )
        serializer.instance = instance
        
    def list(self, request, *args, **kwargs):
        # Override the list method to add full URLs for profile photos
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        
        # Add full URLs for profile photos
        for user_data in data:
            if user_data.get('profile_photo'):
                if not user_data['profile_photo'].startswith('http'):
                    host = request.get_host()
                    protocol = 'https' if request.is_secure() else 'http'
                    user_data['profile_photo'] = f"{protocol}://{host}{user_data['profile_photo']}"
        
        return Response(data)
    


class UserProfilePhotoView(generics.UpdateAPIView):
    """
    Заливка profile_photo в Cloudinary (через cloudinary_storage)
    и возврат обновлённого объекта с готовым URL.
    """
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = FirebaseUserSerializer

    def get_object(self):
        user_id = self.request.query_params.get('user_id')
        obj, _ = FirebaseUser.objects.get_or_create(
            firebase_user_id=user_id,
            defaults={'email': self.request.data.get('email', '')}
        )
        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # Если пришёл файл — сохраняем в Cloudinary
        if 'profile_photo' in request.FILES:
            instance.profile_photo = request.FILES['profile_photo']
            instance.save()

        # Возвращаем только готовый URL в виде JSON
        return Response({
            'profile_photo': instance.profile_photo.url
        })
