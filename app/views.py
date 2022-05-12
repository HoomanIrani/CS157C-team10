import json
from django.shortcuts import render
from django.conf.urls import include
from django.template import loader
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from app.db_api.authentication import authenticate_role
from django.contrib.auth import login as user_login
from app.decorators import student_required, faculty_required, auditor_required, coordinator_required
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .final_new import get_sentiment, get_tags, get_sentiments

from django.db.models import Count,Sum,Avg,IntegerField,Case,When
from django.shortcuts import render_to_response
# import db_populate

#sentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(sentence):
	vs = analyzer.polarity_scores(sentence)
	vs.pop('compound')
	type = max(vs.items(),key=lambda x:x[1])[0]
	print("Sentiment is",type)
	return type

@login_required
def home(request):
    return render(request, 'base-vuetify.html')

@student_required
def student_dashboard(request):
	print("beta")
	feedbackforms = FeedbackForm.objects.filter(is_active=True, is_published=True).all()
	# for ff in feedbackforms:
	# 	print(ff.title)
	context = {
		'numberofforms':len(feedbackforms),
		'feedbackforms':feedbackforms
	}
	return render(request, 'student_dashboard_new_new.html', context)

@student_required
def ajax_student_dashboard(request):
	# print("alpha")
	feedbackforms = FeedbackForm.objects.filter(is_active=True, is_published=True)
	student = request.user.student
	context = {}
	
	for form in feedbackforms:
		# print('form', form.form_id)
		questions = Question.objects.filter(form_id = form.form_id).all()
		# print(questions)
		q_count = len(questions)
		responses = 0	
		for question in questions:
			fr = FeedbackResponse.objects.filter(student_id=student.student_id,question=question.question_id).all()
			# print(fr)
			if len(fr) > 0:
				responses += len(fr)
		# print('form', form.title)
		# print('responses', responses)
		# print('q_count', q_count)
		count = responses
		
		# print("count", count)
		# if count == 0:
		# 	context['form'+str(form.form_id)] = 'Urgent'
		if count < q_count:
			context['form'+str(form.form_id)] = 'Incomplete'
		else:
			context['form'+str(form.form_id)] = 'Complete'
	return JsonResponse(context)

@student_required
def student_profile(request):
	return render(request, 'student_profile_new.html')

@student_required
def events(request):
	return render(request, 'events.html')

@faculty_required
def faculty_dashboard(request):

	context = {} 
	prof_id = request.user.professor.prof_id 
	forms = list(FeedbackForm.objects.filter(is_published=True))
	# course_professor = list(CourseProfessor.objects.filter(prof_id = prof_id))
	compare_tags = {}
	for form in forms:
		questions = []
		questions_objs = Question.objects.filter(form_id = form.form_id).all() 
		for question_obj in questions_objs:
			questions.append(question_obj.question_id)
		feedback_responses = []
		cp_ids = []
		cp_objs = CourseProfessor.objects.filter(prof_id = prof_id).all() #.values_list('prof_id'))
		for cp_obj in cp_objs:
			cp_ids.append(cp_obj.prof_id)
		# print("CP_IDS", cp_ids)
		# print("QUESTIONS", questions)
		prev_feedback_responses = FeedbackResponse.objects.filter(cp_id__in = cp_ids).all()
		# print("prev_feedback_responses", prev_feedback_responses)
		
		
		for question_id in questions:
			# print("Question", question_id)
			feedback_response = prev_feedback_responses.filter(question=question_id).first()
		# 	# print("FEEDBACK RESPONSE", feedback_response)
		# 	if feedback_response.cp_id in cp_ids:
			feedback_responses.append(feedback_response)
		
		# print("Feedback Reponses" , feedback_responses)

		tags = {}
		if feedback_responses:
			for fr in feedback_responses:
				if fr is not None and fr.answer is not None:
					tag_id = Question.objects.filter(question_id = fr.question).first().tag_id
					if tag_id not in tags:
						tags[tag_id] = list()
					tags[tag_id].append(fr.answer)
			# print("tags", tags)		
			for tag_id, list_answers in tags.items():
				if tag_id == None:
					if tag_id not in compare_tags:
						compare_tags[tag_id] = []
					compare_tags[tag_id].append(sum(list_answers)/len(list_answers))
				else:
					tag_title = Tag.objects.filter(tag_id = tag_id).first().tag_title
					if tag_title not in compare_tags:
						compare_tags[tag_title] = []
					compare_tags[tag_title].append(sum(list_answers)/len(list_answers))

			# print("Compare Tags", compare_tags)

			context[form] = {}
			for cp_id in cp_ids:
				course_code = CourseProfessor.objects.filter(cp_id = cp_id).first().course_code
				course_name = Course.objects.filter(course_code = course_code).first().name
				context[form][course_name] = {}
				context[form][course_name]['overall'] = {}

				avg_cp_id_list = {}
				count = {}
				temp_feedback_responses = {}

				for fr in feedback_responses:
					if fr is not None:
						if fr.cp_id not in avg_cp_id_list:
							avg_cp_id_list[cp_id] = []
						avg_cp_id_list[cp_id].append(fr.answer)

						if fr.answer not in count:
							count[fr.answer] = 0
						count[fr.answer] += 1

						if fr.question not in temp_feedback_responses:
							temp_feedback_responses[fr.question] = []
						temp_feedback_responses[fr.question].append(fr.answer)

				print(avg_cp_id_list)
				context[form][course_name]['overall'] = {}
				context[form][course_name]['overall']['avg'] = round(sum(avg_cp_id_list[1])/len(avg_cp_id_list[1]),2)
				context[form][course_name]['overall']['scores'] = {6:{'val':0,'perc':100}}
				maxv = 0
				for i in range(1, 6):
					# print("CONTEXT FORM", context[form])
					context[form][course_name]['overall']['scores'][i] = {}
					if i not in count:
						count[i] = 0
					context[form][course_name]['overall']['scores'][i]['val'] = count[i]
					if maxv < context[form][course_name]['overall']['scores'][i]['val']:
						maxv = context[form][course_name]['overall']['scores'][i]['val']
					context[form][course_name]['overall']['scores'][6]['val'] += context[form][course_name]['overall']['scores'][i]['val']
				if maxv:	
					for i in range(1, 6):
						context[form][course_name]['overall']['scores'][i]['perc'] = int((context[form][course_name]['overall']['scores'][i]['val']/maxv)*100)
				else:
					context[form][course_name]['overall']['scores'][i]['perc'] =0

				context[form][course_name]['responses'] = {}
				context[form][course_name]['strength'] = set()
				context[form][course_name]['weakness'] = set()
				# responses = list(FeedbackResponse.objects.filter(teacher_subject=teacher_subject,question__feedback_form=form))
				responses = feedback_responses
				for response in responses:
					if response is None:
						continue
					question = Question.objects.filter(question_id = response.question).first().text
					#print(question.tag.tag_title)
					context[form][course_name]['responses'][question] = {}
					# temp = list(FeedbackResponse.objects.filter(question=question).values('question').annotate(avg =Avg('answer')))
					
					temp = []
					for key, val in temp_feedback_responses.items():
						temp.append({"question" : key, "avg" : sum(val)/len(val)})
					# print (" TEMP IS ", temp)
					context[form][course_name]['responses'][question]['overall'] = temp[0]['avg']
					context[form][course_name]['responses'][question]['scores'] = {}
					maxv = 0
					for i in range(1,6):
						# print("question", response.question)
						# print("answer",i)

						# birju = FeedbackResponse.objects.filter(question=response.question,answer=i).all()
	
						context[form][course_name]['responses'][question]['scores'][i] = {}
						context[form][course_name]['responses'][question]['scores'][i]['val'] = len(FeedbackResponse.objects.filter(question=response.question,answer=i).all())
						if maxv < context[form][course_name]['responses'][question]['scores'][i]['val']:
							maxv = context[form][course_name]['responses'][question]['scores'][i]['val']
					for i in range(1,6):
						context[form][course_name]['responses'][question]['scores'][i]['perc'] = round((context[form][course_name]['responses'][question]['scores'][i]['val']/maxv)*100,2)
	
			# 		for data in temp:
			# 			tag = Question.objects.filter(question_id = response.question).first().tag_id
			# 			if tag == None:
			# 				continue
			# 			tag_name = Tag.objects.filter(tag_id = tag).first().tag_title
			# 			if(data['avg'] > 3.5):#not working
			# 				# print("adding strength")
			# 				context[form][course_name]['strength'].add(tag_name)
			# 			else:
			# 				# print("adding weakness")
			# 				context[form][course_name]['weakness'].add(tag_name)
			# 		scores= {}
			# 		# for i in range(1,6):
			# 		# 		scores[i] = FeedbackResponse.objects.filter(teacher_subject=teacher_subject, question=question, answer = i).count()
					
			# context[form][course_name]['strength'] = list(
			# 	context[form][course_name]['strength'])
			# context[form][course_name]['weakness'] = list(
			# 	context[form][course_name]['weakness'])
			# while(len(context[form][course_name]['strength']) != len(context[form][course_name]['weakness'])):
			# 	if(len(context[form][course_name]['strength']) < len(context[form][course_name]['weakness'])):
			# 		context[form][course_name]['strength'].append("")
			# 	else:
			# 		context[form][course_name]['weakness'].append("")

			# strength_weakness = []
			# for i in range(len(context[form][course_name]['strength'])):
			# 	strength_weakness.append(
			# 		(context[form][course_name]['strength'][i],
			# 		context[form][course_name]['weakness'][i]))
			# context[form][course_name]['strength_weakness'] = strength_weakness

			# responses = TextualResponse.objects.filter(feedback_form_id=form.form_id)
			# sentiments = {}
			# for response in responses:
			# 	sentiments[response] = get_sentiments(response.answer)

		#print(context)
	graphs=compare_tags
	print ("context ", context)
	return render_to_response( 'faculty_dashboard.html',locals())


@faculty_required
def faculty_profile(request):
	return render(request, 'faculty_profile.html')

@auditor_required
def auditor_profile(request):
	return render(request, 'auditor_profile.html')

@auditor_required
def auditor_dashboard(request):

	context = {}
	forms   = list(FeedbackForm.objects.filter(is_published=True))
	departments = list( Department.objects.all() )
	for form in forms:
		context[form] = {}
		if list(FeedbackResponse.objects.filter(question__feedback_form=form)):
			types = list(QuestionType.objects.all())
			types_overall_rating=list(FeedbackResponse.objects.filter(question__feedback_form =form).values('question__type__title').annotate(avg =Avg('answer')))
			for type_ in types_overall_rating:
				type_['avg']=round(((type_['avg']/5)*100),2)
				if type_['avg'] > 75:
					type_['color'] = 'green'
				elif type_['avg'] > 60:
					type_['color'] = 'orange'
				else:
					type_['color'] = 'red'
			context[form]['types_overall_rating'] =types_overall_rating
		overall_list=FeedbackResponse.objects.filter(question__feedback_form=form).values("question__feedback_form").annotate(avgs=Avg('answer'))[0]
		# print("HELLO WORLD", overall_list)
		overall_list['avgs'] = round(overall_list['avgs'], 2)
		context[form]['scores'] = {}
		context[form]['scores'][6] = {'val':0,'perc':100}
		maxv = 0
		for i in range(1,6):
			context[form]['scores'][i] = {}
			context[form]['scores'][i]['val'] = len(FeedbackResponse.objects.filter(question__feedback_form=form,answer=i).all())
			context[form]['scores'][6]['val'] += context[form]['scores'][i]['val']
			if maxv < context[form]['scores'][i]['val']:
				maxv = context[form]['scores'][i]['val']

		if maxv:
			for i in range(1,6):
				context[form]['scores'][i]['perc'] = round((context[form]['scores'][i]['val']/maxv)*100,2)
		else:
			for i in range(1,6):
				context[form]['scores'][i]['perc'] = 0
					
		context[form]['overall']=overall_list
		context[form]['tags'] = list(Question.objects.filter(feedback_form=form,type__title='Faculty').only('tag'))
		context[form]['score'] = []
		context[form]['columns'] = ["Name", "Dept"]
		de_dupe = {}
		for t in context[form]['tags']:
			if t.tag is not None and t.tag.tag_title not in de_dupe:
				de_dupe[t.tag.tag_title] = 1
				context[form]['columns'].append(t.tag.tag_title)
		context[form]['columns'].append("Overall")

		for faculty in Faculty.objects.all():
			cur_faculty = []
			cur_faculty.append(faculty.profile.name)
			cur_faculty.append(TeacherSubject.objects.filter(teacher=faculty)[0].classroom.department.name)
			
			tag_merge = {}
			for resp in context[form]['tags']:
					cur_resp = list(FeedbackResponse.objects.filter(question__feedback_form=form,
													teacher_subject__teacher=faculty, question=resp)
													.values("question__tag__tag_title")
													.annotate(avgs=Avg('answer')))
					if cur_resp[0]['question__tag__tag_title'] not in tag_merge:
						tag_merge[cur_resp[0]['question__tag__tag_title']] = []
					tag_merge[cur_resp[0]['question__tag__tag_title']].append(cur_resp[0]["avgs"])
			
			print("Akshay tag_merge:", tag_merge)
			tag_score = {}
			overall = 0
			for k, v in tag_merge.items():
				cur_avg = 0
				for val in v:
					cur_avg += val
				cur_avg /= len(v)
				tag_score[k] = round(cur_avg, 2)
				overall += cur_avg
			if tag_score:
				overall /= len(tag_score.keys())
				overall = round(overall, 2)
			print("Akshay tag_score:", tag_score)
			de_dupe = {}
			for resp in context[form]['tags']:
				if resp.tag is not None and resp.tag.tag_title not in de_dupe:
					de_dupe[resp.tag.tag_title] = 1
					cur_tag = resp.tag.tag_title
					cur_faculty.append(tag_score[cur_tag])
			print("Akshay cur_faculty:", cur_faculty)
			cur_faculty.append(overall)
			context[form]['score'].append(cur_faculty)
		print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n\n", context[form])
	
	return render_to_response('auditor_dashboard.html',locals())

@auditor_required
def ajax_data_table(request, formid=None, dept=None, minimum=None, maximum=None):
	if formid:
		if dept:
			if minimum or maximum:
				minimum = max(0,minimum)
				maximum = min(5,maximum)
				faculty_question_data = FeedbackResponse.objects.filter(question__feedback_form__id  = formid).values('teacher_subject__teacher','question__tag').annotate(avg = Avg('answer'))
				print(faculty_question_data)
				return JsonResponse({'x':'y'})
			else:
				return JsonResponse({'x':'y2'})
		else:
			return JsonResponse({'x':'y3'})
	else:
		return JsonResponse({'error':'no formid'})


@coordinator_required
def coordinator_dashboard(request):
	forms = FeedbackForm.objects.all()
	context = {
		'forms':forms
	}
	return render(request, 'coordinator_dashboard.html', context)

@coordinator_required
def publish_form(request, formid):
	form = FeedbackForm.objects.get(pk=formid)
	form.is_published = True
	form.save()
	return redirect('coordinator_dashboard')

@coordinator_required
def activate_form(request, formid):
	form = FeedbackForm.objects.get(pk=formid)
	form.is_active = True
	form.save()
	return redirect('coordinator_dashboard')

@coordinator_required
def deactivate_form(request, formid):
	form = FeedbackForm.objects.get(pk=formid)
	form.is_active = False
	form.save()
	return redirect('coordinator_dashboard')

@coordinator_required
def copy_form(request, formid):
	form = FeedbackForm.objects.filter(form_id = formid).first()
	form.form_id = len(FeedbackForm.objects.all())+ 1
	form.title = form.title + ' - Copy'
	form.is_active = False
	form.is_published = False
	form.save()
	for question in Question.objects.filter(form_id=formid).all():
		print("qid", question.question_id)
		question.question_id = len(Question.objects.all()) + 1
		question.form_id = form.form_id
		question.save()
	return redirect('coordinator_dashboard')

@coordinator_required
def ajax_delete_question(request):
	formid = request.POST['formid']
	qid = request.POST['qid']
	print ("REQUEST ", request)
	Question.objects.get(question_id=qid).delete()
	return JsonResponse({'success':'true'});

@student_required
def ajax_text_response(request):
    text = request.POST['text']
    type = QuestionType.objects.filter(title=request.POST['type']).first().q_type_id
    student_id = request.POST['student']
    if student_id != None:
        student_id = int(request.POST['student'])
    text_response = TextualResponse(
        text_id = len(TextualResponse.objects.all()) + 1,
        student_id = student_id,
        q_type_id=type,
        answer=text,
        feedback_form_id=request.POST['formid'],
        cp_id = None
    )
    text_response.save()
    print('text response saved')

    sentiment = get_sentiment(text)

    return JsonResponse({'sentiment':sentiment})

@coordinator_required
def ajax_predict_tags(request):
	text = request.POST['text']
	tag = get_tags(text)
	print("Tag is", tag)
	if tag != -1:
		tag_obj = Tag.objects.get(tag_id=tag)
		return JsonResponse({'tag':tag_obj.tag_title})
	else:
		return JsonResponse({'tag':''})


@coordinator_required
def edit_form_title(request):
	print("alpha")
	formid = request.POST['formid']
	title = request.POST['title']
	# print("formid", formid)
	# print("title", title)
	form = FeedbackForm.objects.get(form_id = formid)
	form.title = title
	form.save()
	return JsonResponse({'success':'true'})

@coordinator_required
def delete_form(request,formid):
	form = FeedbackForm.objects.get(form_id=formid)
	form.delete()
	return redirect('coordinator_dashboard')

@coordinator_required
def edit_form(request, formid=None):
	ACADEMICS = QuestionType.objects.get(title='Academics').q_type_id
	INFRASTRUCTURE = QuestionType.objects.get(title='Infrastructure').q_type_id
	FACULTY = QuestionType.objects.get(title='Faculty').q_type_id
	if formid:
		form = FeedbackForm.objects.get(form_id = formid)
	else:
		form = FeedbackForm(title='Blank Form', form_id = len(FeedbackForm.objects.all()) + 1, is_published = False, is_active = False)
		form.save()
		return redirect('/edit_form/'+str(form.form_id))
	questions = Question.objects.filter(form_id=form.form_id)
	acadquestions = questions.filter(q_type_id=ACADEMICS)
	infraquestions = questions.filter(q_type_id=INFRASTRUCTURE)
	facultyquestions = questions.filter(q_type_id=FACULTY)
	tags = Tag.objects.all()
	context = {
		'form':form,
		'acadquestions':acadquestions,
		'infraquestions':infraquestions,
		'facultyquestions':facultyquestions,
		'tags':tags
	}
	return render(request, 'edit_questions.html', context)

@coordinator_required
def coordinator_profile(request):
	return render(request, 'coordinator_profile.html')

@coordinator_required
def create_form(request):
	if request.method == 'POST':
		form = CreateNewForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			new_form = FeedbackForm(form_id = len(FeedbackForm.objects.all()) + 1, title=title, is_active = False, is_published = False)
			new_form.save()
			return redirect('add_questions',formid=new_form.id)
	else:
		form = CreateNewForm()
	return render(request, 'create_form.html', {'form':form})

@coordinator_required
def add_questions(request,formid):
	curr_form = FeedbackForm.objects.get(form_id=formid)
	context = {
		'curr_form':curr_form
	}
	return render(request, 'add_questions.html', context)

@coordinator_required
def ajax_add_questions(request):
	print(request.POST)
	data = request.POST
	q = Question(
		question_id = len(Question.objects.all()) + 1,
		text=data['text'],
		tag_id=int(data['tagid']),
		q_type_id=QuestionType.objects.filter(title=data['type']).first().q_type_id,
		feedback_form=int(data['form'])
	)
	q.save()
	
	context = {}
	return redirect('edit_form',data['form'])

@coordinator_required
def edit_form_question(request):
	print(request.POST)
	data = request.POST
	tag_obj = None

	# if data['tagid'] != "":
	# 	tag_obj = Tag.objects.filter(tag_id=int(data['tagid'])).first()
	tag = None
	if data['tagid'] != '':
		tag = int(data['tagid'])
	# print("trying to add a question and qid is ",len(Question.objects.all()))
	q = Question(
		question_id = len(Question.objects.all()) + 1,
		text=data['text'],
		tag_id=tag,
		q_type_id=QuestionType.objects.filter(title=data['type']).first().q_type_id,
		form_id=int(data['formid'])
	)
	q.save()
	
	context = {}
	return redirect('edit_form',data['formid'])


@student_required
def feedback_faculty(request,formid):
	FACULTY = QuestionType.objects.filter(title='Faculty').first().q_type_id
	course_professors = CourseProfessor.objects.all()
	courses = {}
	for cp in course_professors:
		courses[Course.objects.filter(course_code = cp.course_code).first()] = Professor.objects.filter(prof_id = cp.prof_id).first()
	
	print("Courses", courses)
	feedbackform = FeedbackForm.objects.filter(form_id = formid).first()
	questions = Question.objects.filter(form_id=feedbackform.form_id)
	facultyquestions = questions.filter(q_type_id=FACULTY)

	context = {
		'courses': courses,
		'facultyquestions':facultyquestions
	}
	return render(request, 'feedback_faculty.html', context)

@student_required
def student_feedback(request, form_id):
	print("IN STUDENT FEEDBACK")
	print('in student_feedback',form_id)
	ACADEMICS = QuestionType.objects.filter(title='Academics').first().q_type_id
	INFRASTRUCTURE = QuestionType.objects.filter(title='Infrastructure').first().q_type_id
	FACULTY = QuestionType.objects.filter(title='Faculty').first().q_type_id
	print("Academic Questions", ACADEMICS)
	print("Infrastructure Questions", INFRASTRUCTURE)
	print("Professor Questions", FACULTY)
	curr_user = request.user
	feedbackform = FeedbackForm.objects.filter(form_id = form_id).first()
	course_professors = CourseProfessor.objects.all()
	courses = {}
	for cp in course_professors:
		courses[Course.objects.filter(course_code = cp.course_code).first()] = Professor.objects.filter(prof_id = cp.prof_id).first()
	
	print("Courses", courses)
	questions = Question.objects.filter(form_id=feedbackform.form_id)
	acadquestions = questions.filter(q_type_id=ACADEMICS)
	infraquestions = questions.filter(q_type_id=INFRASTRUCTURE)
	
	context = {
		'form':feedbackform,
		'courses': courses,
		'acadquestions':acadquestions,
		'infraquestions':infraquestions,
	}

	return render(request, 'feedback_new.html', context)

@student_required
def student_feedback_response_set(request):
	q_id = request.GET.get('q_id',None)
	s_id = request.GET.get('s_id',None)
	a_val = request.GET.get('a_val',None)

	a_val = int(a_val)

	try:
		fr = FeedbackResponse.objects.filter(question=q_id, student_id=s_id).first()
	except:
		fr = FeedbackResponse(id = len(FeedbackResponse.objects.all()) + 1, question=q_id, student_id=s_id, answer = a_val)
	fr.answer = a_val
	print(fr.answer)
	fr.save()
	
	return JsonResponse({
		'success':'success'
	})

@student_required
def student_feedback_response_get(request):
	q_id = request.GET.get('q_id',None)
	s_id = request.GET.get('s_id',None)
	
	try:
		fr = FeedbackResponse.objects.filter(question=q_id, student_id=s_id).first()
		ansval = fr.answer
		print(ansval)
		return JsonResponse({
			'ans':ansval
		})
	except:
		return JsonResponse({
			'ans':0
		})

@student_required
def student_feedback_faculty_response_set(request):
	print('\n\n\n\n\n\n\n SFFRS called \n\n\n\n\n\n\n')

	q_id = request.GET.get('q_id',None)
	s_id = request.GET.get('s_id',None)
	f_id = request.GET.get('f_id',None)
	sub_id = request.GET.get('sub_id',None)
	a_val = request.GET.get('a_val',None)

	# print ("q_id", q_id)
	# print ("s_id", s_id)
	# print ("f_id", f_id)
	# print ("sub_id", sub_id)
	# print ("a_val", a_val)

	cp_id = CourseProfessor.objects.filter(course_code = sub_id, prof_id = f_id).first().cp_id
	# question = Question.objects.filter(pk=q_id).first()
	# student = Student.objects.filter(pk=s_id).first()
	# faculty = Faculty.objects.filter(pk=f_id).first()
	# subject = Subject.objects.filter(pk=sub_id).first()

	# teacher_subject = TeacherSubject.objects.filter(classroom=student.classroom,teacher=faculty,subject=subject).first()

	# print(q_id, f_id, s_id, sub_id, a_val, question, student, faculty, subject, teacher_subject)
	a_val = int(a_val)

	count = len(FeedbackResponse.objects.all()) + 1

	try:
		fr = FeedbackResponse.objects.filter(student_id = s_id, question = q_id, cp_id = cp_id).first()
		if fr is None:
			raise Exception
		# fr = FeedbackResponse.objects.get(student=student,question=question,teacher_subject=teacher_subject)
	except:
		fr = FeedbackResponse(id = count, student_id = s_id, question = q_id, answer = a_val, cp_id = cp_id)
	fr.answer = a_val
	print(fr.answer)
	fr.save()
	
	return JsonResponse({
		'success':'success'
	})

@student_required
def student_feedback_faculty_response_get(request):
	q_id = request.GET.get('q_id',None)
	s_id = request.GET.get('s_id',None)
	f_id = request.GET.get('f_id',None)
	sub_id = request.GET.get('sub_id',None)
	print("SUB ID", sub_id)
	course = Course.objects.filter(course_code=sub_id).first()

	course_professor = CourseProfessor.objects.filter(course_code = course.course_code, prof_id = f_id).first()
	
	try:
		fr = FeedbackResponse.objects.filter(student_id=s_id,question=q_id,cp_id=course_professor.cp_id).first()
		ansval = fr.answer
		print(ansval)
		return JsonResponse({
			'ans':ansval
		})
	except:
		return JsonResponse({
			'ans':0
		})		

@student_required
def feedback_faculty_theory(request):
	curr_user = request.user
	teachings = TeacherSubject.objects.filter(classroom=curr_user.student.classroom)
	courses = {teaching.subject:teaching.teacher for teaching in teachings}
	pass

@student_required
def feedback_infrastructure(request):
	#add form here and redirect to page
	pass

@student_required
def feedback_academics(request):
	#add form here and redirect to page
	pass

def signup(request):
	"""	if request.method == 'POST':
			form = SignUpForm(request.POST)
			if form.is_valid():
				user = form.save()
				user.refresh_from_db()  # load the profile instance created by the signal
				user.student.role = "student"
				user.student.student_name = form.cleaned_data.get('student_name')
				user.student.email = form.cleaned_data.get('email')
				user.student.phone_number = form.cleaned_data.get('phone_number')
				raw_password = form.cleaned_data.get('password1')
				user.student.save()
				user = authenticate(username=user.username, password=raw_password)
				login(request, user)
				return redirect('home')

		else:
			form = SignUpForm()
		return render(request, 'signup.html', {'form': form})
	"""
	pass

def login(request):

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
				elif (role == 'FACULTY'):
					return redirect('faculty_dashboard')
				elif(role == 'COORDINATOR'):
					return redirect('coordinator_dashboard')

			else:
				messages.error(request, 'Username or Password Incorrect')

	else:
		form=LogInForm()
	return render(request, 'login_new.html', {'form': form})


def logout_view(request):
	logout(request)
	return redirect('login')

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            #messages.success(request, 'Your password was successfully updated!')
            role=authenticate_role(user)

            if(role == 'STUDENT'):
                return redirect('student_dashboard')
            elif (role == 'FACULTY'):
                return redirect('faculty_dashboard')
            elif(role == 'COORDINATOR'):
                return redirect('coordinator_dashboard')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })

import json
from django.db.models import Sum,Count
from django.core import serializers
def test_graph(request):
	"""academic_response =  FeedbackResponse.objects.filter(question__type__title="Academics").values('question').annotate(dsum=Sum('answer'),dcount = Count('student'))
				context = serializers.serialize('json', academic_response)
			"""
	return render(request, 'test_graph.html')
