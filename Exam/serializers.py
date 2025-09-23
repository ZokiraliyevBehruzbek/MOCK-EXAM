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
    listening = ListeningTestSerializer(read_only=True)
    reading = ReadingTestSerializer(read_only=True)
    writing = WritingTestSerializer(read_only=True)

    class Meta:
        model = Exam
        fields = "__all__"
