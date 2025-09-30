from rest_framework import serializers
from .models import ListeningTest, ReadingTest, WritingTest, Exam, UserExamSession


class ListeningTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListeningTest
        exclude = ['answers']


class ReadingTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingTest
        exclude = ['answers']


class WritingTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WritingTest
        fields = "__all__"


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        # serializer ichiga koshsa user examen boshlagandan oldin savollarni kurolaydi
        exclude = ['listening', 'reading', 'writing', 'allowed_users', 'joined_users'] 

class UserExamSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserExamSession
        exclude = []