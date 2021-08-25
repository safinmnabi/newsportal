from django.shortcuts import render, redirect
from .models import Users, Settings
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from newsapi import NewsApiClient
import sendgrid
import os, json, requests, time, datetime, random
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import math
from sendgrid.helpers.mail import *
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt



     # Account Register, Login and Logout System
#---------------Start------------------#

def register(request):
	if request.session['isLogged'] == True:
		return redirect('home')

	if request.method == 'POST':
		fname = request.POST.get('fname')
		email = request.POST.get('email')
		pwd = request.POST.get('pwd')
		passhass = make_password(pwd)

		if Users.objects.filter(email=email).count()>0:
			messages.error(request,'Email is already exists.')
			return redirect('register')
		else:

			user = Users(fullname=fname, email=email, password=passhass)
			user.save()

			settings = Settings(userid=email)
			settings.save()
			return redirect('login')
	else:
		return render(request, 'register.html')


def login(request):
	if request.session['isLogged'] == True:
		return redirect('home')

	if request.method == 'POST':
		email = request.POST.get('email')
		pwd = request.POST.get('pwd')

		try:
			check_user = Users.objects.get(email=email)

			if check_password(pwd, check_user.password):
				request.session['user'] = email
				request.session['fullname'] = check_user.fullname
				request.session['isLogged'] = True
				return redirect('home')
			else:
				messages.error(request,'You entered wrong password')
				return redirect('login')

		except:
			messages.error(request,'This email is not found in system and please register this email')
			return redirect('login')

	else:
		request.session['isLogged'] = False
		if request.session['isLogged']:
			return redirect('login')
		else:
			return render(request, 'login.html' )

def logout(request):
	try:
		del request.session['user']
		del request.session['fullname']
		request.session['isLogged'] = False
	except:
		return redirect('login')
	return redirect('login')

#------------------------end----------------------------#



#User who forgot password will send email account
#---------------Start---------------------#

def reset_password(request):
	if request.session['isLogged'] == True:
		return redirect('home')

	if request.method == 'POST':

		email = request.POST.get('email')
		expire_time = datetime.datetime.now() + datetime.timedelta(minutes = 15)
		expire_token = expire_time.timestamp()
		hashs = random.getrandbits(128)

		try:
			user = Users.objects.get(email=email)
			user_update = Users(id=user.id, fullname=user.fullname, email=email, password=user.password, token=hashs, expire_token=expire_token)
			user_update.save()

			generate_link = os.environ.get('APP_URL')+"/check/"+email+"/"+str(hashs)
			data = {'username': user.fullname,'link': generate_link}
			recover_email(email, data)

			messages.error(request,'Email for reset password request already Sent')
			return redirect('recover')

		except Exception as e:
			print(e)
			messages.error(request,'This email is not found in system')
			return redirect('recover')

	if request.session['isLogged'] == True:
		return redirect('home')
	else:
		return render(request, 'reset_password.html' )

#------------------------end----------------------------#



	#To send email for reseting password
#---------------Start---------------------#


def recover_email(email, data):

	subject = "Sending Password Recover"
	html_content = get_template('token.html').render(data)
	content = Content("text/html", html_content)
	message = Mail(from_email=os.environ.get('SENDGRID_FROM_EMAIL'), subject=subject, to_emails=email, html_content=content)
	try:
		sg = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_API'))
		response = sg.send(message)
		code, body, headers = response.status_code, response.body, response.headers
	except Exception as e:
		print("Error: {0}".format(e))

	return response.status_code

#------------------------end----------------------------#



#User will have to enter and re-enter password
#---------------Start---------------------#

def changepassword(request, email, token):

	if request.method == 'POST':
		pass1 = request.POST.get('pass1')
		pass2 = request.POST.get('pass2')

		if pass1 == pass2:
			passhass = make_password(pass1)
			user = Users.objects.get(email=email)
			user_update = Users(id=user.id, fullname=user.fullname, email=email, password=passhass, token=None, expire_token=None)
			user_update.save()
			messages.error(request,'Password is changed succesfully')
			return redirect('login')

		else:
			messages.error(request,'Password is not matched.')
			return render(request, 'change_password.html' )

		

	user = Users.objects.get(email=email)
	if token == user.token:
		if datetime.datetime.now().timestamp() < float(user.expire_token):
			messages.error(request,'Token is Verified.')
			return render(request, 'change_password.html' )
		else:
			messages.error(request,'Token is expired and please re-enter email to send again.')
			return redirect('login')
	else:
		messages.error(request,'Token is invalid.')
		return redirect('login')

#------------------------end----------------------------#



#To fetch data from newsapi to store data
#---------------Start---------------------#

def news_fetch(request):

	newsapi = NewsApiClient(api_key='1de1186491cd4fd989e88e38f213db4b')

	country = ['us']
	source = []
	keyword = []
	news_store = []

	try:
		settings = Settings.objects.get(userid=request.session['user'])
		country = settings.country
		if country == None or country == '':
			country = ['us']
		else:
			country = country.split(',')
		
		source = settings.source
		if source == None or source == '':
			source = []
		else:
			source = source.split(',')

		keyword = settings.keyword
		if keyword == None or keyword == '':
			keyword = []
		else:
			keyword = keyword.split(',')

	except Exception as e:
		print(e)
		country = ['us']
		source = []
		keyword = []
		news_store = []
	

	for i in country:
		sources = newsapi.get_top_headlines(country=i, page_size=100)
		for x in sources['articles']:
			if source == []:
				desc = x["description"]
				if keyword == []:
					x["source"].update({"country":i})
					news_store.append(x)
				else:
					if any(ks in desc for ks in keyword):
						x["source"].update({"country":i})
						news_store.append(x)					
			else:
				for s in source:				
					desc = x["description"]
					if keyword == []:
						if x["source"]["id"] == s:
							x["source"].update({"country":i})
							news_store.append(x)
					else:
						if any(ks in desc for ks in keyword):
							if x["source"]["id"] == s:
								x["source"].update({"country":i})
								news_store.append(x)
	return news_store

#------------------------end----------------------------#



	#Home Page for showing newsletter
#---------------Start---------------------#

def home(request):
	if request.session['isLogged'] == False:
		return redirect('login')

	data = news_fetch(request);
	context = []

	newsletter(request)

	fname = request.session['fullname']


	for n in range(8):
		if n == len(data):
			break
		else:
	  		context.append({
				"title": data[n]["title"],
				"country": data[n]["source"]["country"],
				"source": data[n]["source"]["name"],
				"desc":  data[n]["description"],
				"url": data[n]["url"],
				"image": data[n]["urlToImage"],
			})


	total_news = len(data)
	total_pags = math.ceil(total_news/8.0)
	defualtid=1
	prevBtn = False
	nextBtn = True

	if total_news < 8:
		nextBtn = False

	message = {"text":"", "status":True}
	if total_news  == 0:
		message["status"] = False
		message["text"] = "No news is available"


	scheduler_time = 600
	pag = {"prev": (defualtid-1), "prevBtn": prevBtn, "nexp": (defualtid+1), "nextBtn": nextBtn, "total_pags": range(1,int(total_pags)+1), "c_pag":defualtid}


	return render(request, 'newspage.html', {'data':context, 'fname': fname, 'pags':pag, 'error':message, "schedule":scheduler_time})

#------------------------end----------------------------#



#To show previous page, next page, current in Homepage
#---------------Start---------------------#

def pagination(request,id):
	  
	data = news_fetch(request);
	context = []

	total_news = len(data)

	total_pags = math.ceil(total_news/8.0)
	print(math.ceil(total_pags))

	last_pag = 8*id;
	prev_pag = (last_pag - 8)

	prevBtn = False
	nextBtn = True

	if last_pag > total_news:
		balance_news = last_pag - total_news
		last_pag = last_pag - balance_news
		nextBtn = False

	if prev_pag > 0:
		prevBtn = True
	
	for n in range(prev_pag, last_pag):
		context.append({
			"title": data[n]["title"],
			"country": data[n]["source"]["country"],
			"source": data[n]["source"]["name"],
			"desc":  data[n]["description"],
			"url": data[n]["url"],
			"image": data[n]["urlToImage"],
		})

	fname = request.session['fullname']	

	message = {"text":"", "status":True}
	if total_news  == 0:
		message["status"] = False
		message["text"] = "No news is available"

	pag = {"prev": (id-1), "prevBtn": prevBtn, "nexp": (id+1), "nextBtn": nextBtn, "total_pags": range(1,int(total_pags)+1), "c_pag":id}


	return render(request, 'newspage.html', {'data':context, 'fname':fname, 'pags':pag, 'error':message})
#----------------End----------------------#




#----------------Setting System for filtering country, source and keyword-----------------#
#---------------Start---------------------#


def setting(request):
	userid = request.session['user']
	uid = Settings.objects.get(userid=userid)
	if request.method == 'POST':
		user_id = request.POST.get('id')
		country = request.POST.get('country')
		source = request.POST.get('source')
		keyword = request.POST.get('keyword')
		user = Settings(id=user_id,country=country, source=source, keyword=keyword, userid=userid)
		user.save()
		return redirect('home')
	else:
		pass

	fname = request.session['fullname']
	return render(request, 'setting.html', {'fname':fname,'userid': userid, 'uid': uid})

#----------------End----------------------#



#----------------To send email notification when to change setting-----------------#
#---------------Start---------------------#

def newsletter(request):

	user_id = request.session['user']
	settings = Settings.objects.get(userid=user_id)
	keyword = False
	if settings.keyword == None or settings.keyword == '':
		keyword = False
	else:
		keyword = True

	data = news_fetch(request)
	context = []

	if keyword:
		if len(data) != 0:
			for n in range(len(data)):
				context.append({
					"title": data[n]["title"],
					"country": data[n]["source"]["country"],
					"source": data[n]["source"]["name"],
					"desc":  data[n]["description"],
					"url": data[n]["url"],
					"image": data[n]["urlToImage"],
				})

			subject = "New Newsletter"
			html_content = get_template('newsletter.html').render({'data':context})
			content = Content("text/html", html_content)
			message = Mail(from_email=os.environ.get('SENDGRID_FROM_EMAIL'), subject=subject, to_emails=user_id, html_content=content)
			try:
				sg = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_API'))
				response = sg.send(message)
				code, body, headers = response.status_code, response.body, response.headers
				print(response.status_code)
				print(response.body)
				print(response.headers)
			except Exception as e:
				print("Error: {0}".format(e))	

			return response.status_code

#----------------End----------------------#



#---------------- Exposing Api to client/user  -----------------#
#---------------Start---------------------#

@csrf_exempt
def api(request):
	if request.method == 'POST':
		email = request.POST.get('email')
		pwd = request.POST.get('pwd')

		try:
			check_user = Users.objects.get(email=email)

			if check_password(pwd, check_user.password):
				request.session['user'] = email
				data = news_fetch(request)
				context = []

				for n in range(len(data)):
					context.append({
						"title": data[n]["title"],
						"country": data[n]["source"]["country"],
						"source": data[n]["source"]["name"],
						"desc":  data[n]["description"],
						"url": data[n]["url"],
						"image": data[n]["urlToImage"],
					})
				return JsonResponse(context, safe=False)

			else:
				return JsonResponse({"message":'You entered wrong password', 'status': False})

		except:
			return JsonResponse({"message":'This email is not found in system and please register this email', 'status': False})
			

	
	return JsonResponse({"message":'Unauthorized Zone', 'status': False})

#----------------End----------------------#
