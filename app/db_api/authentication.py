from app.models import  Profile, Student, Professor, CourseProfessor
def authenticate_role(user):
	# if Student username exists and password is matching:
	# 	return "student"
	# elif Faculty username exists and password is matching:
	# 	return "faculty's role"
	# else:
	# 	return -1
   
    #print ("is in authentication.py")
    if hasattr(user, 'student'):
        #print (user.student.type)
        return user.student.type
    elif hasattr(user, 'professor'):
        return user.professor.type
    elif hasattr(user, 'coordinator'):
        return user.coordinator.type
    else:
        return -1
