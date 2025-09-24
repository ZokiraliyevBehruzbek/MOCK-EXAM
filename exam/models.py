from django.db import models
from users.models import User


class ListeningTest(models.Model):
    questions = models.JSONField()   # list ko‘rinishida saqlash
    audio = models.FileField(upload_to="listening/")
    answers = models.JSONField()

    def __str__(self):
        return f"Listening Test {self.id}"


class ReadingTest(models.Model):
    text_field = models.TextField()
    questions = models.JSONField()
    answers = models.JSONField()

    def __str__(self):
        return f"Reading Test {self.id}"


class WritingTest(models.Model):
    question1 = models.TextField()
    question2 = models.TextField()


    def __str__(self):
        return f"Writing Test {self.id}"


class Exam(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

   
    users = models.ManyToManyField(User, related_name="exams")

    is_public = models.BooleanField(default=False)

    listening = models.ForeignKey(ListeningTest, on_delete=models.SET_NULL, null=True, blank=True)
    reading = models.ForeignKey(ReadingTest, on_delete=models.SET_NULL, null=True, blank=True)
    writing = models.ForeignKey(WritingTest, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Exam {self.id}"
