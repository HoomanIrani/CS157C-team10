from django.shortcuts import render
from .forms import LogInForm
from django.contrib.auth import authenticate  #login, logout,
from django.contrib.auth import login as user_login
from app.db_api.authentication import authenticate_role
from django.shortcuts import render, redirect
from django.contrib import messages

def login(request):
	# ACADEMICS = QuestionType.objects.get(title='Academics')
	# INFRASTRUCTURE = QuestionType.objects.get(title='Infrastructure')
	# FACULTY = QuestionType.objects.get(title='Faculty')
	if request.method == 'POST':
		form=LogInForm(request.POST)
		if form.is_valid():
			user=form
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				user_login(request, user)
				role=authenticate_role(user)

				if(role == 'STUDENT'):
					return redirect('student_dashboard')
				elif (role == 'PROFESSOR'):
					return redirect('professor_dashboard')
				elif(role == 'COORDINATOR'):
					return redirect('coordinator_dashboard')

			else:
				messages.error(request, 'Username or Password Incorrect')

	else:
		form=LogInForm()
	return render(request, 'login_new.html', {'form': form})

#@coordinator_required
def coordinator_dashboard(request):
	return render(request, 'coordinator_dashboard.html')


#@student_required
def student_dashboard(request):
	return render(request, 'student_dashboard_new.html')

#@professor_required
def professor_dashboard(request):

	return render(request, 'professor_dashboard_new.html')