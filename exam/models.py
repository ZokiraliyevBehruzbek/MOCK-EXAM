from django.db import models
from users.models import User


class ListeningTest(models.Model):
    md_file = models.TextField()
    audio = models.FileField(upload_to="listening/")
    answers = models.JSONField()

    def __str__(self):
        return f"Listening Test {self.id}"


class ReadingTest(models.Model):
    md_file = models.TextField()
    answers = models.JSONField()

    def __str__(self):
        return f"Reading Test {self.id}"


class WritingTest(models.Model):
    question1 = models.TextField()
    question2 = models.TextField()

    def __str__(self):
        return f"Writing Test {self.id}"


class Exam(models.Model):
    exam_name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    allowed_users = models.ManyToManyField(User, related_name="allowed_exams")
    joined_users = models.ManyToManyField(User, related_name="exams")
    
    is_public = models.BooleanField(default=False)

    listening = models.ForeignKey(ListeningTest, on_delete=models.SET_NULL, null=True, blank=True)
    reading = models.ForeignKey(ReadingTest, on_delete=models.SET_NULL, null=True, blank=True)
    writing = models.ForeignKey(WritingTest, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Exam {self.id}"


class UserExamSession(models.Model):
    user = models.ForeignKey(User, related_name='exam_sessions', on_delete=models.CASCADE)
    exam = models.ForeignKey(User, related_name='sessions', on_delete=models.CASCADE)

    listening_started_at = models.DateTimeField(null=True, blank=True)
    reading_started_at = models.DateTimeField(null=True, blank=True)
    writing_started_at = models.DateTimeField(null=True, blank=True)

    listening_finished = models.BooleanField(default=False)
    reading_finished = models.BooleanField(default=False)
    writing_finished = models.BooleanField(default=False)

TEST_TYPES = models.TextChoices('types', 'listening reading writing')

class TestResult(models.Model):
    answers = models.JSONField()
    user = models.ForeignKey(User, related_name='results', on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, related_name='results', on_delete=models.CASCADE)
    test_type = models.TextField(choices=TEST_TYPES)