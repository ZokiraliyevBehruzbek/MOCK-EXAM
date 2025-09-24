from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListeningTestViewSet, ReadingTestViewSet, WritingTestViewSet, ExamViewSet

router = DefaultRouter()
router.register(r'listening-tests', ListeningTestViewSet)
router.register(r'reading-tests', ReadingTestViewSet)
router.register(r'writing-tests', WritingTestViewSet)
router.register(r'exams', ExamViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
