from rest_framework import generics, permissions
from .models import Project
from .serializers import ProjectSerializer
from .permissions import IsOwnerOrReadOnly

class ProjectListCreateView(generics.ListCreateAPIView):
    """
    GET /api/projects/ -> list
    POST /api/projects/ -> create (owner ست می‌شود به request.user)
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # هنگام ایجاد، owner را از کاربر درخواست بگیر
        serializer.save(owner=self.request.user)


class ProjectRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET /api/projects/<pk>/ -> retrieve
    PUT/PATCH/DELETE -> update/delete (فقط توسط owner)
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]