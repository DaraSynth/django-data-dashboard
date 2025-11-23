from django.urls import path
from .views import ProjectListCreateView, ProjectRetrieveUpdateDeleteView

urlpatterns = [
    path('projects/', ProjectListCreateView.as_view(), name='project-list'),
    path('projects/<int:pk>/', ProjectRetrieveUpdateDeleteView.as_view(), name='project-detail'),
]