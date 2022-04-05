from django.db import models
from django.contrib.auth.models import User

PROFILE_TYPES = (
    (u'STUDENT', 'Student'),
    (u'PROFESSOR', 'Professor'),
    (u'COORDINATOR', 'Coordinator')
)

class Course(models.Model):
    course_id = models.IntegerField()
    course_name = models.TextField(max_length = 50)

#common field resides here
class Profile(models.Model):
    name = models.TextField(max_length = 250)
    email = models.EmailField(max_length = 254, blank=True)
    phone_number = models.CharField(max_length=13, blank=True)
    def __str__(self):
        return self.name

class Professor(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    profile = models.OneToOneField(Profile,on_delete = models.CASCADE)
    type = models.CharField(choices=PROFILE_TYPES, max_length=16, default = 'PROFESSOR')
    prof_id = models.IntegerField() #primary key
    prof_name = models.TextField(max_length=250)
    courses = models.ManyToManyField(Course, on_delete = models.CASCADE)

class CourseProfessor(models.Model):
    cp_id = models.IntegerField() #primary key
    prof_id = models.ForeignKey(Professor, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)

# used just to define the relation between User and Profile
class Student(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    profile = models.OneToOneField(Profile,on_delete = models.CASCADE)
    type = models.CharField(choices=PROFILE_TYPES, max_length=16, default = 'STUDENT')
    course_professor = models.ManyToManyField(CourseProfessor, on_delete = models.CASCADE)
    def __str__(self):
        return self.profile.name