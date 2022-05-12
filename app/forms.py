from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import *

class LogInForm(forms.Form):

	username = forms.CharField(
		label='Username',
		max_length=50,
		help_text='Enter username',
		widget=forms.TextInput(
			attrs= {
				'class': 'validate'
			}
		)
	)

	password = forms.CharField(
		label='Password',
		max_length=50,
		help_text='Enter Password',
		widget=forms.TextInput(
			attrs={
				'class': 'validate',
				'type': 'password'
			}
		)
	)
	class Meta:
		fields = ['username','password']
		widgets = {
			'username':forms.TextInput(),
			'password':forms.PasswordInput(),
		}

class CreateNewForm(forms.Form):
	title = forms.CharField(
		label='Form Name',
		max_length=50,
		help_text='Enter form name',
		widget=forms.TextInput(
			attrs={
				'id':'form_name'
			}
		)
	)