from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from datetime import timedelta
from .models import ListeningTest, ReadingTest, WritingTest, Exam, UserExamSession, TestResult
from django.utils import timezone
from .serializers import (
    ListeningTestSerializer, ReadingTestSerializer,
    WritingTestSerializer, ExamSerializer
)
from .permissions import IsAdminOrReadOnly, IsUserInExam
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
    queryset = Exam.objects.filter(is_public=True)
    serializer_class = ExamSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=["post"], url_path="join", permission_classes=[IsAuthenticated])
    def join_exam(self, request, pk=None):
        exam = self.get_object()
        user = request.user

        if exam.start_time > timezone.now() or exam.end_time < timezone.now():
            return Response({"detail": "not the right time"}, status=status.HTTP_400_BAD_REQUEST)

        if not user in exam.allowed_users.all() and not exam.is_public:
            return Response({"detail": "You are not allowed"}, status=status.HTTP_400_BAD_REQUEST)

        exam.joined_users.add(user)
        return Response({"detail": "Successfully joined the exam."}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'], url_path='leave', permission_classes=[IsAuthenticated])
    def leave_exam(self, request, pk=None):
        exam = self.get_object()
        exam.joined_users.get(id=request.user.id).delete()
        return Response({"detail": "you left the exam"})
    
    @action(detail=True, methods=['post'], url_path='start-listening', permission_classes=[IsAuthenticated])
    def start_listening(self, request, pk=None):
        exam = self.get_object()
        user = request.user

        if exam.started_at > timezone.now() or exam.end_time < timezone.now():
            raise PermissionDenied('not the right time')
        if not user in exam.joined_users.all():
            return Response({"detail": "You have not joined"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            UserExamSession.objects.get(exam=exam, user=user)
            raise PermissionDenied("you already started listening")
        except UserExamSession.DoesNotExist:
            pass

        UserExamSession.objects.create(exam=exam, user=user, listening_started_at=timezone.now())

        serializer = ListeningTestSerializer(exam.listening)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='finish-listening', permission_classes=[IsAuthenticated])
    def finish_listening(self, request, pk=None):
        exam = self.get_object()
        user = request.user
        answers = request.data

        try:
            session = UserExamSession.objects.get(exam=exam, user=user)
            if timezone.now() - session.listening_started_at > timedelta(minutes=32):
                raise PermissionDenied("Too late. Womp Womp")
            TestResult.objects.create(user=user, 
                                      exam=exam, 
                                      test_type='listening', 
                                      answers=answers) 
            session.listening_finished = True
            session.save()
            return Response({"detail": "Congratulations! Go on now to reading!"})
        except:
            raise PermissionDenied("did you even start listening?")
    
    @action(detail=True, methods=['post'], url_path='start-reading', permission_classes=[IsAuthenticated])
    def start_reading(self, request, pk=None):
        exam = self.get_object()
        user = request.user

        try:
            session = UserExamSession.objects.get(exam=exam, user=user)
            if session.listening_finished:
                raise PermissionDenied("you have already finished listening")
            if not session.listening_finished:
                # listening tugatib, reading boshlash kerak
                raise PermissionDenied("you haven't finsihed listening")
            session.reading_started_at = timezone.now()
            session.save()
        except UserExamSession.DoesNotExist:
            raise PermissionDenied("reading not started")

        serializer = ReadingTestSerializer(exam.reading)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='finish-reading', permission_classes=[IsAuthenticated])
    def finish_reading(self, request, pk=None):
        exam = self.get_object()
        user = request.user
        answers = request.data

        try:
            session = UserExamSession.objects.get(exam=exam, user=user)
            if session.reading_finished:
                raise PermissionDenied("reading already finished")
            if timezone.now() - session.reading_started_at > timedelta(minutes=60):
                raise PermissionDenied("Too late. Womp Womp")
            TestResult.objects.create(user=user, 
                                      exam=exam, 
                                      test_type='reading', 
                                      answers=answers)
            session.reading_finished = True
            session.save()
            return Response({"detail": "Congratulations! Go on now to writing!"})
        except:
            raise PermissionDenied("did you even start listening?")
    
    @action(detail=True, methods=['post'], url_path='start-writing', permission_classes=[IsAuthenticated])
    def start_writing(self, request, pk=None):
        exam = self.get_object()
        user = request.user

        try:
            session = UserExamSession.objects.get(exam=exam, user=user)
            if not session.reading_finished:
                raise PermissionDenied("you haven't finished reading")
            session.writing_started_at = timezone.now()
            session.save()
        except UserExamSession.DoesNotExist:
            raise PermissionDenied("exam session has not been started, first start listening to create a start session")
        
        serializer = WritingTestSerializer(exam.writing)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='finish-writing', permission_classes=[IsAuthenticated])
    def finish_writing(self, request, pk=None):
        exam = self.get_object()
        user = request.user
        answers = request.data

        try:
            session = UserExamSession.objects.get(exam=exam, user=user)
            if timezone.now() - session.writing_started_at > timedelta(minutes=60):
                raise PermissionDenied("Too late. Womp Womp")
            TestResult.objects.create(user=user, 
                                      exam=exam, 
                                      test_type='writing', 
                                      answers=answers)
            session.delete()
            return Response({"detail": "That's it! Just wait for the results!"})
        except:
            raise PermissionDenied("did you even start listening?")