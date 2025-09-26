from rest_framework import serializers
from .models import ListeningTest, ReadingTest, WritingTest, Exam


class ListeningTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListeningTest
        fields = "__all__"


class ReadingTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingTest
        fields = "__all__"


class WritingTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WritingTest
        fields = "__all__"


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = "__all__"
        # serializer ichiga koshsa user examen boshlagandan oldin savollarni kurolaydi
        exclude = ['listening', 'reading', 'writing', 'allowed_users', 'joined_users'] 
