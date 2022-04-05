from app.models import  Profile, Student, Professor, CourseProfessor
def authenticate_role(user):
	# if Student username exists and password is matching:
	# 	return "student"
	# elif Faculty username exists and password is matching:
	# 	return "faculty's role"
	# else:
	# 	return -1
    """ try:
        obj = Student.objects.get(user = user)
    except Student.DoesNotExist:
        obj = None
    if(obj is not None):
        print('student was here')
        return 'Student'
    else:
        obj = Employee.objects.get(user = user)

        if(obj.role == 'Faculty'):
            return 'Faculty'       
        else:
            return 'Co-ordinator' """

    #print ("is in authentication.py")
    if hasattr(user, 'Student'):
        #print (user.student.type)
        return user.student.type
    elif hasattr(user, 'Professor'):
        return user.faculty.type
    elif hasattr(user, 'Coordinator'):
        return user.coordinator.type
    else:
        return -1
