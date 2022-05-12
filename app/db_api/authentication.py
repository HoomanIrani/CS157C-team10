from app.models import *
def authenticate_role(user):
	
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
