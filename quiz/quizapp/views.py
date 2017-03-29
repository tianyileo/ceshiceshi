from django.shortcuts import render,redirect,render_to_response
from .models import ZhangJie,Question,userFenshu,UserProfile,userFenshu,Answer
from datetime import datetime

from .forms import LoginForm,RegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
# Create your views here.

def home(request):
    context = {}
    return render(request,"home.html",context)



def practice(request):
    context = {}
    zhangjie_list = ZhangJie.objects.all()
    context['zhangjie_list'] = zhangjie_list
    return  render(request,'practice.html',context)


def show_question_by_zhangjie(request,zhangjie):
    context = {}
    #question = Question.objects.get(zhangjie=fenlei,id=q_id)
    question_list_by_zhangjie = Question.objects.filter(zhangjie__slug=zhangjie)
    context['question_list_by_zhangjie'] = question_list_by_zhangjie
    return render(request , 'question-zhangjie-id.html',context)


def show_question_by_id(request,id):
    context = {}
    #question = Question.objects.get(zhangjie=fenlei,id=q_id)
    question = Question.objects.get(id=id)
    context['question'] = question
    return render(request , 'question-id.html',context)




def quiz(request):
	fenshu = 0
	r_count = 0
	w_count = 0
	w_obj_list = []
	r_obj_list = []
	user_sc_select = ''
	user_mc_select = []
	context = {}
	user = request.user
	if request.method == "POST":
		info = request.POST
		#print(info)  的值是一个{question——id：answers——id，。。。。。。}
		print(info)
		for q in info:
		#字典的循环取值，http://www.cnblogs.com/skyhacker/archive/2012/01/27/2330177.html 只是先把key取出来
			tmp = []
			try:
				print(info[q])
				tmp = Question.objects.get(id=q)
				#answer_list = tmp.answer_set.all()
				if tmp.leixing == 1:
					if info[q] == str(tmp.get_right_answer()[0].id)  :
						r_count += 1
						#print('before')
						#print(tmp.right_count)
						#print(tmp.get_right_answer())
						tmp.right_count += 1
						#print(q)
						#print(info[str(q)])
						user_sc_select = Answer.objects.get(id = info[str(q)])
						context['user_sc_select'] = user_sc_select
						r_obj_list.append(tmp)
					else:
						w_count += 1
						tmp.wrong_count += 1
						#print(q)
						#print(tmp.get_right_answer()[0])
						#print(tmp.get_right_answer()[0].id)
						w_obj_list.append(tmp)
						#print(info[str(q)])
						user_sc_select = Answer.objects.get(id = info[str(q)])
						context['user_sc_select'] = user_sc_select
						tmp.save()
				else:
					#print(tmp.id)
					#print(request.POST.getlist(str(tmp.id)))
					user_select= []
					for yyyy in request.POST.getlist(str(tmp.id)):
						user_select.append(int(yyyy))
					#print(new_list1)
					#print('tmp.get_right_answer()的值是什么-')
					#print(tmp.get_right_answer().values_list('id', flat=True))
					right_select_list = list(tmp.get_right_answer().values_list('id', flat=True))
					#print(type(mmm))
					#print(type(list(mmm)))
					if user_select == right_select_list:
						r_count += 1
						tmp.right_count += 1
						#print(info.getlist(q))
						user_mc_selects = Answer.objects.filter(pk__in = info.getlist(q))
						for user_mc_select_a in user_mc_selects:
							#print(user_mc_select_a)
							user_mc_select.append(Answer.objects.get(id = info[str(user_mc_select_a)]))
						context['user_mc_select'] = user_mc_select
						r_obj_list.append(tmp)
						#print(user_mc_select)
					else:
						w_count += 1
						tmp.wrong_count += 1
						w_obj_list.append(tmp)
						user_mc_selects = Answer.objects.filter(pk__in = info.getlist(q))
						for user_mc_select_id in user_mc_selects:
							user_mc_select.append(user_mc_select_id.title)
						context['user_mc_select'] = user_mc_select
						tmp.save()
			except:
				pass

	if r_count + w_count == 0:
		return render(request,'error.html')
	else:
		fenshu = 100*r_count/(r_count + w_count)
		record = userFenshu(user=user,pub_date=datetime.now(),fenshu=fenshu,notes="",zhangjie = '')
		record.save()
		if fenshu == 100:
			for r_q in r_obj_list:
				zhangjie = r_q.zhangjie.zhangjie_title
		else:
			for w_q in w_obj_list:
				record.wrong_question.add(w_q)
				zhangjie = w_q.zhangjie.zhangjie_title
		record.zhangjie = zhangjie
		record.save()

	context['fenshu'] = fenshu
	context['r_count'] = r_count
	context['w_count'] = w_count
	context['w_obj_list'] = w_obj_list
	context['select_zhangjie'] = zhangjie
	#context['user_sc_select'] = info[q]
	fenshu_list = []
	xzhou_list = []
	zhangjie_list = []

	obj_list_email = userFenshu.objects.all().order_by('-id').filter(user = user)

	for obj in obj_list_email:
		fenshu_list.append(obj.fenshu)
		zhangjie_list.append(obj.zhangjie)
	context['fenshu_list'] = fenshu_list
	for i in range(len(fenshu_list),0,-1):
		xzhou_list.append('第{}次考试'.format(i))
	context['xzhou_list'] = xzhou_list
	context['obj_list_email']=obj_list_email


	email_list = []
	for xxx,yyy,zzz in zip(xzhou_list,zhangjie_list,fenshu_list):
		email_list.append('{}-------章节：{}------成绩：{}'.format(xxx,yyy,zzz))
	# print(email_list)
	# email_list = 'tianyi'
	msg_plain = render_to_string('email.txt', {'email_list': email_list,'user':user})
	msg_html = render_to_string('email.html', {'email_list': email_list,'user':user})
	send_mail(
		'{}的成绩单'.format(user),
		msg_plain,
		'jinhelichao@163.com',
		['3252436793@qq.com'],
		html_message=msg_html,
		)
	#context['user_mc_select'] = user_select
	#return render_to_response("quiz.html",variables)
	return render(request,"quiz.html",context)


@login_required(login_url='/login/')
def quiz_create(requset):
	obj_list = []
	isCreated = False
	quiz_info=""
	context={}
	if requset.method == "POST":
		#leixing = requset.POST['leixing']
		#zhangjie = requset.POST['zhangjie']
		zhangjie = requset.POST.get('zhangjie')
		#q_num = requset.POST['q_num']
		q_num = requset.POST.get('q_num')
		# print(leixing)
		context['q_num'] = q_num
		context['zhangjie'] = zhangjie

		if( zhangjie and q_num ):
			## create a quiz with q_num questions.
			isCreated = True
			_class=""

			#新版中 我把类型除掉了
			obj_list = Question.objects.filter(zhangjie=zhangjie).order_by('?')[:int(q_num)]

	context['obj_list'] = obj_list
	context['isCreated'] = isCreated

	return render(requset,"quiz-create.html",context)

# 这里不能把函数命名为login，否则与内置的login冲突
def index_login(request):
    context = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            try:
                username = User.objects.get(email=email).username
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)

                    # 跳到登陆前的页面
                    referer = request.GET.get("referer", None)
                    if referer is None:
                        return redirect(to="home")
                    return redirect(referer)
            except Exception as e:
                print(e)
    return render(request, "login.html", context)

def register(request):
    context = {}
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            name = form.cleaned_data["name"]
            password = form.cleaned_data["password"]

            # 判断相同名称用户是否存在，如果不存在则允许注册
            users = User.objects.filter(username=name)
            if len(users) == 0:
                user = User()
                user.username = name
                user.email = email
                user.is_staff = True
                user.set_password(password)
                user.save()

                # 同时还需要创建用户扩展信息， 否则会提示request.user.profile不存在
                userprofile = UserProfile(belong_to=user, name=name, email=email)
                userprofile.save()

                #  找到最后一次访问页面，排除掉注册页面本身
                if "REFERER" in request.META and "/register" in request.META["REFERER"]:
                    return redirect(to="login", referer=request.META["REFERER"])
            return redirect(to="login")
        return redirect(to="register")
    return render(request, "register.html", context)

@login_required(login_url='/login/')
def show_record(request):
	context ={}
	user = request.user
	fenshu_list = []
	xzhou_list = []

	obj_list = userFenshu.objects.all().order_by('-id').filter(user = user)

	for obj in obj_list:
		fenshu_list.append(obj.fenshu)
		#print(obj.get_question_zhangjie())

	#print(fenshu_list)
	context['fenshu_list'] = fenshu_list
	for i in range(len(fenshu_list),0,-1):
		xzhou_list.append('第{}次考试'.format(i))
	#print(xzhou_list)
	context['xzhou_list'] = xzhou_list
	context['obj_list']=obj_list
	#发邮件的功能在这个地方不合适  挪到了quiz函数中
	email_list = []
	for xxx,yyy in zip(xzhou_list,fenshu_list):
		email_list.append('{}:{}'.format(xxx,yyy))
	print(email_list)
	context['email_list']=email_list
	# # email_list = 'tianyi'
	# msg_plain = render_to_string('email.txt', {'email_list': email_list,'user':user})
	# msg_html = render_to_string('email.html', {'email_list': email_list,'user':user})
	# #print(obj_list.get(id =218).user)
	# #print(obj_list.get(id =218).pub_date)
	# #print(obj_list.get(id =218).fenshu)
	# #print(list(obj_list.get(id =218).wrong_question.all())[0].zhangjie)
	# #print(obj_list.get(id =1))
	# #print(obj_list.get(id =1).wrong_question.get(id =1))
    #
	# send_mail(
	# 	'{}的成绩单'.format(user),
	# 	msg_plain,
	# 	'jinhelichao@163.com',
	# 	['3252436793@qq.com'],
	# 	html_message=msg_html,
	# 	)
	#send_mail('subject', email_list, 'jinhelichao@163.com',['3252436793@qq.com'], fail_silently=False)
	return render(request,"record.html",context)

def page_not_found(request):
	response =  render_to_response('404.html')
	response.status_code = 404
	return response

def page_error(request):
	response =  render_to_response('500.html')
	response.status_code = 500
	return response
#以下为复制的原来项目中的
#coding=utf-8
# from django.http import HttpResponseRedirect
# #from django.shortcuts import render_to_response
# from django.shortcuts import render,redirect,get_object_or_404
# from django.template import RequestContext
# from quiz.models import *
# from datetime import datetime
# from quiz.forms import LoginForm,RegisterForm
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
#
#
#
# def show_question_by_id(request,q_id):
# 	obj = ''
# 	context= {}
# 	try:
# 		obj = Question.objects.get(id=q_id)
# 		#obj = get_object_or_404(Question,id = q_id)
# 		#print(type(obj.id))
# 		#print(obj.id)
# 	except:
#
# 		return redirect(to="show_question_by_id", q_id = int(q_id)-1)
# 	#variables = RequestContext(request,{'obj':obj})
# 	context['obj'] = obj
# 	#return render_to_response("question.html",variables)
# 	return render(request,"question.html",context)
#
#
#
# def show_all_questions(request):
# 	obj_list = []
# 	context= {}
# 	try:
# 		obj_list = Question.objects.all().order_by('-id')
# 	except:
# 		pass
# 	#variables = RequestContext(request,{'obj_list':obj_list})
# 	context['obj_list'] = obj_list
# 	#return render_to_response("q_all.html",variables)
# 	return render(request,"q_all.html",context)
# @login_required(login_url='/login/')
# def quiz_create(requset):
# 	obj_list = []
# 	isCreated = False
# 	quiz_info=""
# 	context={}
# 	if requset.method == "POST":
# 		leixing = requset.POST['leixing']
# 		zhangjie = requset.POST['zhangjie']
# 		q_num = requset.POST['q_num']
# 		# print(leixing)
# 		# print(zhangjie)
# 		# print(q_num)
# 		# print(type(leixing))
# 		# print(type(zhangjie))
# 		# print(type(q_num))
# 		if( leixing and zhangjie and q_num ):
# 			## create a quiz with q_num questions.
# 			isCreated = True
# 			_class=""
#
# 			# if(zhangjie=="1"):
# 			# 	_class=u'Cultural Diversity'
# 			# elif ( zhangjie=="2"):
# 			# 	_class=u'End-of-Life Care'
# 			# elif (zhangjie=="3"):
# 			# 	_class=u'Ethical/Legal'
# 			# elif (zhangjie=="3"):
# 			# 	_class=u'Ethical/Legal'
# 			# elif (zhangjie=="3"):
# 			# 	_class=u'Ethical/Legal'
#
# 			# quiz_info = u'类型：%s,  章节：%s,  题目数目：%s个' % (leixing,_class,q_num)
# 			## obj_list - generate here.
# 			## just for test
# 			#obj_list = Question.objects.all().filter(leixing=leixing,zhangjie=zhangjie)
# 			obj_list = Question.objects.filter(leixing=leixing,zhangjie=zhangjie).order_by('?')[:int(q_num)]
# 			#obj_list = Question.objects.all().filter(leixing=leixing,zhangjie=zhangjie).order_by('?')[:int(q_num)]
# 	#variables = RequestContext(requset,{'obj_list':obj_list,'isCreated':isCreated,'quiz_info':quiz_info})
# 	context['obj_list'] = obj_list
# 	context['isCreated'] = isCreated
# 	# context['quiz_info'] = quiz_info
# 	#return render_to_response("quiz-create.html",variables)
# 	return render(requset,"quiz-create.html",context)
#
# def quiz(request):
# 	result = 0
# 	r_count = 0
# 	w_count = 0
# 	w_obj_list = []
# 	context = {}
# 	user = request.user
# 	if request.method == "POST":
# 		info = request.POST
# 		#print(info)  的值是一个{question——id：answers——id，。。。。。。}
# 		for q in info:
# 		#字典的循环取值，http://www.cnblogs.com/skyhacker/archive/2012/01/27/2330177.html 只是先把key取出来
# 			tmp = []
# 			print(q)
# 			try:
# 				tmp = Question.objects.get(id=q)
# 				### 目前仅支持单选类别，未来需要加上判断题目类型，如果
# 				### 是多选则进行for循环依次判断答案是否正确
# 				if ( info[q] == str(tmp.get_right_answer()[0].id) ):
# 					r_count += 1
# 					print('before')
# 					print(tmp.right_count)
# 					tmp.right_count += 1
# 					print('after')
# 					print(tmp.right_count)
# 				else:
# 					w_count += 1
# 					tmp.wrong_count += 1
# 					w_obj_list.append(tmp)
# 				tmp.save()
# 			except:
# 				pass
# 	if(r_count+w_count):
# 		result = 100*r_count/(r_count + w_count)
# 	record = Record(user=user,pub_date=datetime.now(),result=result,notes="",)
# 	record.save()
# 	for w_q in w_obj_list:
# 		record.wrong_question.add(w_q)
# 	record.save()
#
# 	#variables = RequestContext(request,{
# 	#	'result':result,
# 	#	'r_count':r_count,
# 	#	'w_count':w_count,
# 	#	'w_obj_list':w_obj_list,})
# 	context['result']=result
# 	context['r_count']=r_count
# 	context['w_count']=w_count
# 	context['w_obj_list']=w_obj_list
# 	#return render_to_response("quiz.html",variables)
# 	return render(request,"quiz.html",context)
#
# @login_required(login_url='/login/')
# def show_record(request):
# 	context ={}
# 	user = request.user
# 	fenshu_list = []
# 	xzhou_list = []
# 	obj_list = Record.objects.all().order_by('-id').filter(user = user)
# 	#variables = RequestContext(request,{'obj_list':obj_list})
# 	for p in Record.objects.filter(user = user):
# 		print(p.result)
# 		fenshu_list.append(p.result)
# 	print(fenshu_list)
# 	context['fenshu_list'] = fenshu_list
# 	for i in range(1,len(fenshu_list)+1):
# 		xzhou_list.append('第{}次考试'.format(i))
# 	print(xzhou_list)
# 	context['xzhou_list'] = xzhou_list
# 	context['obj_list']=obj_list
# 	print(Record.objects.all().count())
# 	return render(request,"record.html",context)
# # 这里不能把函数命名为login，否则与内置的login冲突
# def index_login(request):
# 	context = {}
# 	if request.method == "POST":
# 		form = LoginForm(request.POST)
# 		if form.is_valid():
# 			name = form.cleaned_data["name"]
# 			email = form.cleaned_data["email"]
# 			password = form.cleaned_data["password"]
# 			try:
# 				#username = User.objects.get(email=email).username
# 				#user = authenticate(username=username, password=password)
# 				user = authenticate(username=name, password=password,email=email)
# 				if user is not None:
# 					login(request, user)
# 					# 跳到登陆前的页面
# 					referer = request.GET.get("referer", None)
# 					if referer is None:
# 						#return redirect(to="home")
# 						return redirect(to="quiz_create")
# 					return redirect(referer)
# 			except Exception as e:
# 				print(e)
# 	return render(request, "login.html", context)
# def register(request):
# 	context = {}
# 	if request.method == "POST":
# 		form = RegisterForm(request.POST)
# 		if form.is_valid():
# 			email = form.cleaned_data["email"]
# 			name = form.cleaned_data["name"]
# 			password = form.cleaned_data["password"]
# 			# 判断相同名称用户是否存在，如果不存在则允许注册
# 			users = User.objects.filter(username=name)
# 			if len(users) == 0:
# 				user = User()
# 				user.username = name
# 				user.email = email
# 				user.is_staff = True
# 				user.set_password(password)
# 				user.save()
# 				# 同时还需要创建用户扩展信息， 否则会提示request.user.profile不存在
# 				userprofile = UserProfile(belong_to=user, name=name, email=email)
# 				userprofile.save()
# 				#  找到最后一次访问页面，排除掉注册页面本身
# 				if "REFERER" in request.META and "/register" in request.META["REFERER"]:
# 					return redirect(to="login", referer=request.META["REFERER"])
# 			return redirect(to="login")
# 		return redirect(to="register")
# 	return render(request, "register.html", context)
