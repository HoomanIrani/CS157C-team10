from operator import index
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator, MaxLengthValidator
from cassandra.cqlengine import columns
from django_cassandra_engine.models import DjangoCassandraModel

PROFILE_TYPES = (
    (u'STUDENT', 'Student'),
    (u'Professor', 'Prodessor'),
    (u'COORDINATOR', 'Coordinator')
)

#common field resides here
class Profile(models.Model):
    name = models.TextField(max_length = 250)
    email = models.EmailField(max_length = 254, blank=True)
    phone_number = models.CharField(max_length=13, blank=True)
    def __str__(self):
        return self.name

# used just to define the relation between User and Profile
class Student(models.Model):
    student_id = models.IntegerField()
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    profile = models.OneToOneField(Profile,on_delete = models.CASCADE)
    type = models.CharField(choices=PROFILE_TYPES, max_length=16, default = 'STUDENT')
    def __str__(self):
        return self.profile.name

class Professor(models.Model):
    prof_id = models.IntegerField()
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    profile = models.OneToOneField(Profile,on_delete = models.CASCADE)
    type = models.CharField(choices=PROFILE_TYPES, max_length=16, default = 'FACULTY')
    def __str__(self):
        return self.profile.name

#profile for coordinator
class Coordinator(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    profile = models.OneToOneField(Profile,on_delete = models.CASCADE)
    type = models.CharField(choices=PROFILE_TYPES, max_length=16, default = 'COORDINATOR')
    def __str__(self):
        return self.profile.name

class Course(DjangoCassandraModel):
    course_code= columns.Text(primary_key=True)
    name = columns.Text(required=True)
    def __str__(self):
        return self.course_code , " " ,self.name

#following class is to link faculty with classroom and students
#Teaches changed to TeacherSubject
class CourseProfessor(DjangoCassandraModel):
    cp_id = columns.Integer(primary_key=True)
    course_code = columns.Text(required=True)
    prof_id = columns.Integer(required=True)
    def __str__(self):
        return self.cp_id , " " ,self.course_code, " " ,self.prof_id

class Tag(DjangoCassandraModel):
    tag_id = columns.Integer(primary_key=True)
    tag_title = columns.Text(required=True, index = True)
    def __str__(self):
        return self.tag_title

# for academics/ infrastructure / Faculty
class QuestionType(DjangoCassandraModel):
    q_type_id = columns.Integer(primary_key=True)
    title = columns.Text(required=True, index = True)
    def __str__(self):
        return self.title

class FeedbackForm(DjangoCassandraModel):
    form_id = columns.Integer(primary_key=True)
    title = columns.Text(required=True)
    is_active = columns.Boolean(default=False, required = True)
    is_published = columns.Boolean(default=False, required = True)

    def __str__(self):
        return self.title + "-is_active :" + str(self.is_active) + " is_published:" + str(self.is_published)

class Question(DjangoCassandraModel):
    question_id = columns.Integer(primary_key=True)
    text = columns.Text(required=True)
    q_type_id = columns.Integer(required=True)
    tag_id = columns.Integer(required=False)
    form_id = columns.Integer(required=True, index = True)
    def __str__(self):
        return self.question_id , " " ,self.text, " " ,self.q_type_id

class FeedbackResponse(DjangoCassandraModel):
    id = columns.Integer(primary_key=True)
    student_id = columns.Integer(required=True)
    question = columns.Integer(required=True)
    answer = columns.Integer(required=True)
    cp_id = columns.Integer(required=False)
    def __str__(self):
        return str("self.id")

class TextualResponse(DjangoCassandraModel):
    text_id = columns.Integer(primary_key=True)
    student_id = columns.Integer(required=True)
    q_type_id = columns.Integer(required=True)
    cp_id = columns.Integer(required=False)
    answer = columns.Text(required=True)
    feedback_form_id = columns.Integer(required=True)
    def str(self):
        return self.student_id , " " ,self.q_type_id, " " ,self.cp_id
