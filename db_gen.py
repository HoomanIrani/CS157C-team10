from app import models

# add more courses
COURSES = {
    'NoSQL Database Systems':'CS157C',
}

def creating_subjects():
    print("***CREATING COURSES***")
    cp_id = 1
    for name, code in COURSES.items():
        sub = models.Course(cp_id=cp_id, name=name, course_code=code) 
        sub.save()
        cp_id + 1

FACULTIES = {
    'professor1':{
        'id':1,
        'name':'Akshay Gurnaney',
        'email':'akshay@sjsu.edu',
        'phone_number':'9494949494',
    }
}

def creating_faculties():
    print("***CREATING PROFESSORS***")
    for username,details in FACULTIES.items():
        user = models.User.objects.create_user(username,password='admin123')
        user.save()
        profile = models.Profile(name=details['name'],email=details['email'], phone_number=details['phone_number'])
        profile.save()
        professor = models.Professor(prof_id = details['id'],user=user,profile=profile)
        professor.save()

COURSE_PROFESSORS = {
    1 : {
        'course_code' : 'CS157C',
        'professor_id' : 1,
    }    
}

def creating_course_professor():
    print("***CREATING COURSES***")
    for id, details in COURSE_PROFESSORS.items():
        cp = models.CourseProfessor(
            cp_id = id,
            course_code = details['course_code'],
            prof_id = details['professor_id'],
        )
        cp.save()

COORDINATORS = {
    'coordinator1':{
        'name':'Abhishek Gaikwad',
        'email':'abhishek@sjsu.com',
        'phone_number':'9494949494'
    }
}

def creating_coordinators():
    print("***CREATING CO-ORDINATORS***")
    for username,details in COORDINATORS.items():
        user = models.User.objects.create_user(username,password='admin123')
        user.save()
        profile = models.Profile(
            name=details['name'],
            email=details['email'],
            phone_number=details['phone_number']
        )
        profile.save()
        coordinator = models.Coordinator(
            user=user,
            profile=profile,
        )
        coordinator.save()


STUDENTS = {
    'student1':{
        'name':'Houman Irani',
        'email':'houman@sjsu.edu',
        'phone_number':'9494949494'
    }
}

def creating_students():
    print("***CREATING STUDENTS***")
    s_id = 1
    for username,details in STUDENTS.items():
        user = models.User.objects.create_user(username,password='admin123')
        user.save()
        profile = models.Profile(
            name=details['name'],
            email=details['email'],
            phone_number=details['phone_number']
            )
        profile.save()
        student = models.Student(
            student_id = s_id,
            user=user,
            profile=profile,
        )
        student.save()
        s_id += 1


# def student_dictionary(filename):
#     students = open(filename,'r').read().split('\n')
#     retdict = {}
#     for student in students[1:]:
#         student = student.split(',')
#        # print(student)
#         retdict[student[0]] = {
#             'name':student[1],
#             'email':student[2],
#             'phone_number':student[3],
#             'year':student[4].split(' ')[0],
#             'div':student[4].split(' ')[1]
#         }
#     return retdict

# def creating_students():
#     for roll_no,details in student_dictionary('DataSet1.csv').items():
#         user = models.User.objects.create_user(roll_no,password='admin123')
#         user.save()

#         profile = models.Profile(
#             name=details['name'],
#             email=details['email'],
#             phone_number=details['phone_number']
#         )
#         profile.save()

#        # print(models.Classroom.objects.all())
#         classroom = models.Classroom.objects.all()[0]

#         student = models.Student(
#             user=user,
#             profile=profile,
#             classroom=classroom
#         )
#         student.save()




# def creating_teachersubject():
#     classroom = models.Classroom.objects.all()[0]
#     for teacher,subject in zip(
#         models.Faculty.objects.all(),
#         models.Subject.objects.all()
#     ):
#         teachersubject = models.TeacherSubject(
#             teacher=teacher,
#             subject=subject,
#             classroom=classroom
#         )
#         teachersubject.save()


creating_subjects()
creating_students()
creating_faculties()
creating_coordinators()
creating_course_professor()

