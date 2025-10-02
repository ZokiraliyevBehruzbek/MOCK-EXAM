from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from datetime import timedelta
from .models import ListeningTest, ReadingTest, WritingTest, Exam, UserExamSession, TestResult
from django.utils import timezone
from django.db.models import Q
from .serializers import (
    ListeningTestSerializer, ReadingTestSerializer,
    WritingTestSerializer, ExamSerializer, UserExamSessionSerializer
)
from .permissions import IsAdminOrReadOnly, IsUserInExam, IsExamNotOver
from rest_framework.permissions import IsAuthenticated


class ListeningTestViewSet(viewsets.ModelViewSet):
    queryset = ListeningTest.objects.all()
    serializer_class = ListeningTestSerializer
    permission_classes = [IsAdminUser]


class ReadingTestViewSet(viewsets.ModelViewSet):
    queryset = ReadingTest.objects.all()
    serializer_class = ReadingTestSerializer
    permission_classes = [IsAdminUser]


class WritingTestViewSet(viewsets.ModelViewSet):
    queryset = WritingTest.objects.all()
    serializer_class = WritingTestSerializer
    permission_classes = [IsAdminUser]


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = self.queryset
        queryset = queryset.filter(Q(allowed_users__pk=self.request.user.id) | Q(is_public=True))
        queryset = queryset.exclude(joined_users__pk=self.request.user.id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'], url_path='session', permission_classes=[IsAuthenticated])
    def my_session(self, request, *args, **kwargs):
        exam = self.get_queryset().get(pk=kwargs.pop('pk'))
        user = request.user
        try:
            session = UserExamSession.objects.get(user=user, exam=exam)
            serializer = UserExamSessionSerializer(session)
            return Response(serializer.data)
        except UserExamSession.DoesNotExist:
            return Response({ "detail": "You do not have a session for this exam" }, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'], url_path='joined-exams', permission_classes=[IsAuthenticated])
    def show_exams_user_joined(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset().filter(joined_users__pk=request.user.pk), many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="join", permission_classes=[IsAuthenticated])
    def join_exam(self, request, *args, **kwargs):
        exam = self.get_object()
        user = request.user

        if exam.start_time < timezone.now():
            return Response({"detail": "exam already started"}, status=status.HTTP_400_BAD_REQUEST)

        if not exam.is_public and user not in exam.allowed_users.all():
            return Response({"detail": "You are not allowed"}, status=status.HTTP_400_BAD_REQUEST)
        
        exam.joined_users.add(user)
        return Response({"detail": "Successfully joined the exam."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], url_path='leave', permission_classes=[IsAuthenticated, IsUserInExam])
    def leave_exam(self, request, *args, **kwargs):
        exam = self.get_object()
        exam.joined_users.remove(request.user)
        return Response({"detail": "You left the exam."})

    @action(detail=True, methods=['post'], url_path='start-listening', permission_classes=[IsAuthenticated, IsUserInExam, IsExamNotOver])
    def start_listening(self, request, *args, **kwargs):
        exam = self.get_object()
        user = request.user

        if exam.start_time > timezone.now():
            raise PermissionDenied('not the right time')

        if not UserExamSession.objects.filter(exam=exam, user=user).exists():
            UserExamSession.objects.create(exam=exam, user=user, listening_started_at=timezone.now())

        serializer = ListeningTestSerializer(exam.listening)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='finish-listening', permission_classes=[IsAuthenticated, IsUserInExam, IsExamNotOver])
    def finish_listening(self, request, *args, **kwargs):
        exam = self.get_object()
        user = request.user
        answers = request.data

        try:
            session = UserExamSession.objects.get(exam=exam, user=user)
            if timezone.now() - session.listening_started_at > timedelta(minutes=32):
                raise PermissionDenied("Too late. Womp Womp")

            TestResult.objects.create(user=user, exam=exam, test_type='listening', answers=answers)
            session.listening_finished = True
            session.save()
            return Response({"detail": "Congratulations! Go on now to reading!"})
        except UserExamSession.DoesNotExist:
            raise PermissionDenied("did you even start listening?")

    @action(detail=True, methods=['post'], url_path='start-reading', permission_classes=[IsAuthenticated, IsUserInExam, IsExamNotOver])
    def start_reading(self, request, *args, **kwargs):
        exam = self.get_object()
        user = request.user

        try:
            session = UserExamSession.objects.get(exam=exam, user=user)
            if session.reading_finished:
                raise PermissionDenied("you have already finished reading")
            if not session.listening_finished:
                raise PermissionDenied("you haven't finished listening")
            if not session.reading_started_at:
                session.reading_started_at = timezone.now()
                session.save()

        except UserExamSession.DoesNotExist:
            raise PermissionDenied("listening not started")

        serializer = ReadingTestSerializer(exam.reading)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='finish-reading', permission_classes=[IsAuthenticated, IsUserInExam, IsExamNotOver])
    def finish_reading(self, request, *args, **kwargs):
        exam = self.get_object()
        user = request.user
        answers = request.data

        try:
            session = UserExamSession.objects.get(exam=exam, user=user)
            if session.reading_finished:
                raise PermissionDenied("reading already finished")
            if timezone.now() - session.reading_started_at > timedelta(minutes=60):
                raise PermissionDenied("Too late. Womp Womp")

            TestResult.objects.create(user=user, exam=exam, test_type='reading', answers=answers)
            session.reading_finished = True
            session.save()
            return Response({"detail": "Congratulations! Go on now to writing!"})
        except UserExamSession.DoesNotExist:
            raise PermissionDenied("did you even start listening?")

    @action(detail=True, methods=['post'], url_path='start-writing', permission_classes=[IsAuthenticated, IsUserInExam, IsExamNotOver])
    def start_writing(self, request, *args, **kwargs):
        exam = self.get_object()
        user = request.user

        try:
            session = UserExamSession.objects.get(exam=exam, user=user)
            if not session.reading_finished:
                raise PermissionDenied("you haven't finished reading")

            if not session.writing_started_at:
                session.writing_started_at = timezone.now()
                session.save()
        except UserExamSession.DoesNotExist:
            raise PermissionDenied("exam session has not been started, first start listening")

        serializer = WritingTestSerializer(exam.writing)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='finish-writing', permission_classes=[IsAuthenticated, IsUserInExam, IsExamNotOver])
    def finish_writing(self, request, *args, **kwargs):
        exam = self.get_object()
        user = request.user
        answers = request.data

        try:
            session = UserExamSession.objects.get(exam=exam, user=user)
            if timezone.now() - session.writing_started_at > timedelta(minutes=60):
                raise PermissionDenied("Too late. Womp Womp")

            TestResult.objects.create(user=user, exam=exam, test_type='writing', answers=answers)
            exam.joined_users.remove(user)
            return Response({"detail": "That's it! Just wait for the results!"})
        except UserExamSession.DoesNotExist:
            raise PermissionDenied("did you even start writing?")
