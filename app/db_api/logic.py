from app.models import Course, User
import json

def collect_feedback(data):
    print('-=-=-=-=-=-=-=-=-')
    keys = data.keys()

    for val in data:
        data = json.loads(val)

    student = User.objects.get(username=data['student']).student
    teaches = Teaches.objects.filter(classroom=student.classroom)
    scores = data['formdata']

    print(student)
    print(scores)

    for index,teach in enumerate(teachersubject):
        fftobj = FeedbackFacultyTheory(
            student=student,
            faculty=teach,
            attribute1=scores['#TQ1S'+str(index+1)],
            attribute2=scores['#TQ2S'+str(index+1)],
            attribute3=scores['#TQ3S'+str(index+1)],
            attribute4=scores['#TQ4S'+str(index+1)],
            attribute5=scores['#TQ5S'+str(index+1)],
            attribute6=5,
            attribute7=5
        )
        fftobj.save()