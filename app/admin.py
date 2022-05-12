from django.contrib import admin
from .models import *
admin.site.register(Course)
admin.site.register(Profile)
admin.site.register(Student)
admin.site.register(Professor)
admin.site.register(CourseProfessor)
admin.site.register(Coordinator)
admin.site.register(Tag)
admin.site.register(QuestionType)
admin.site.register(FeedbackForm)
admin.site.register(Question)
admin.site.register(FeedbackResponse)
admin.site.register(TextualResponse)