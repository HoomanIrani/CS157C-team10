from django.contrib import admin

from .models import Course, Profile, Professor, CourseProfessor, Student
admin.site.register(Course)
admin.site.register(Profile)
admin.site.register(Professor)
admin.site.register(CourseProfessor)
admin.site.register(Student)