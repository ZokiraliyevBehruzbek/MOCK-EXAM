from rest_framework import viewsets
from .models import ListeningTest, ReadingTest, WritingTest, Exam
from .serializers import (
    ListeningTestSerializer, ReadingTestSerializer,
    WritingTestSerializer, ExamSerializer
)
from .permissions import IsAdminOrReadOnly


class ListeningTestViewSet(viewsets.ModelViewSet):
    queryset = ListeningTest.objects.all()
    serializer_class = ListeningTestSerializer
    permission_classes = [IsAdminOrReadOnly]


class ReadingTestViewSet(viewsets.ModelViewSet):
    queryset = ReadingTest.objects.all()
    serializer_class = ReadingTestSerializer
    permission_classes = [IsAdminOrReadOnly]


class WritingTestViewSet(viewsets.ModelViewSet):
    queryset = WritingTest.objects.all()
    serializer_class = WritingTestSerializer
    permission_classes = [IsAdminOrReadOnly]


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.filter(is_public=True)
    serializer_class = ExamSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        exam = serializer.save()
        exam.users.add(self.request.user)
