from django.contrib import admin
from exam.models import *

# Register your models here.
admin.site.register(Exam)
admin.site.register(ListeningTest)
admin.site.register(ReadingTest)
admin.site.register(WritingTest)
admin.site.register(TestResult)
admin.site.register(UserExamSession)