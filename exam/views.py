from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ListeningTest, ReadingTest, WritingTest, Exam
from .serializers import (
    ListeningTestSerializer, ReadingTestSerializer,
    WritingTestSerializer, ExamSerializer
)
from .permissions import IsAdminOrReadOnly, IsUserInExam
from rest_framework.permissions import IsAuthenticated


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
<<<<<<< HEAD

    def perform_create(self, serializer):
        exam = serializer.save()
        exam.users.add(self.request.user)

    @action(detail=True, methods=["post"], url_path="join", permission_classes=[IsAuthenticated])
    def join_exam(self, request, pk=None):
        exam = self.get_object()
        user = request.user

        if user in exam.users.all():
            return Response({"detail": "You already joined this exam."}, status=status.HTTP_400_BAD_REQUEST)

        exam.users.add(user)
        return Response({"detail": "Successfully joined the exam."}, status=status.HTTP_200_OK)


    @action(detail=True, methods=["post"], url_path="finish")
    def finish_exam(self, request, pk=None):
        exam = self.get_object()
        user = request.user

        if user not in exam.users.all():
            return Response({"detail": "You are not part of this exam."}, status=status.HTTP_403_FORBIDDEN)

        return Response(
            {"detail": f"{user.username} finished the exam {exam.exam_name}."},
            status=status.HTTP_200_OK
        )
=======
>>>>>>> 9b5db8b (stop using AI)
