from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Course, Student
from .forms import CreateNewCourse, RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="/login")
def home(response):
	return render(response, 'main/home.html')

def index(response, id):
	course = Course.objects.get(id=id)
	if course in response.user.course.all():
		if response.method == "POST":
			if response.POST.get("save"):
				for std in course.student_set.all():
					if response.POST.get('r' + str(std.id)) == "Male":
						std.sex = True
					else:
						std.sex = False
					std.name = response.POST.get('n' + str(std.id))
					std.address = response.POST.get('address' + str(std.id))
					std.save()

			elif response.POST.get("newStudent"):
				name = response.POST.get("newName")
				if response.POST.get("newSex") == "Male":
					sex = True
				else:
					sex = False
				date = response.POST.get("newDOB")
				address = response.POST.get("newAddress")
				if len(name) > 2 and len(date) > 0:
					course.student_set.create(name=name, sex=sex, DOB=date, address=address)
				course.save()
			
			elif response.POST.get("delete"):
				studentID = response.POST.get("delete")
				student = course.student_set.get(id=studentID)
				student.delete()

		return render(response, 'main/list.html', {'course':course})
	return render(response, 'main/view.html', {})

def view(response):
	if response.method == "POST":
		if response.POST.get("C_delete"):
			courseID = response.POST.get("C_delete")
			course = Course.objects.get(id=courseID)
			course.delete()

	return render(response, 'main/view.html', {})

def create(response):
	if response.method == 'POST':
		form = CreateNewCourse(response.POST)
		if form.is_valid():
			course = form.save(commit=False)
			course.save()
			response.user.course.add(course)
			return HttpResponseRedirect("/list_student=%i" %course.id)
	else:
		form = CreateNewCourse()
	return render(response, 'main/create.html', {'form':form})

def register(response):
	if response.method == "POST":
		form = RegisterForm(response.POST)
		if form.is_valid():
			user = form.save()
			login(response, user)
			return redirect("/login")
	else:
		form = RegisterForm()

	return render(response, 'registration/register.html', {'form':form})