from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ToDoList, Item
from .forms import CreateNewList
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(response, id):
	ls = ToDoList.objects.get(id=id)
	if ls in response.user.todolist.all():
		if response.method == "POST":
			print(response.POST)
			if response.POST.get("save"):
				for item in ls.item_set.all():
					if response.POST.get("c" + str(item.id)) == "clicked":
						item.complete = True
					else:
						item.complete = False
					item.text = response.POST.get("t" + str(item.id))
					item.save()
					
			elif response.POST.get("newItem"):
				txt = response.POST.get("new")
				if len(txt) > 2:
					ls.item_set.create(text=txt, complete=False)
				else:
					print("invalid")


			elif response.POST.get("deleteItem"):
				itemID = response.POST.get("deleteItem")
				item = ls.item_set.get(id=itemID)
				item.delete()

		return render(response, "main/list.html", {"ls":ls})
	return render(response, "main/view.html", {})

def create(response):
	if response.method == 'POST':
		form = CreateNewList(response.POST)
		if form.is_valid():
			n = form.cleaned_data["name"]
			t = ToDoList(name=n)
			t.save()
			response.user.todolist.add(t)
		return HttpResponseRedirect("/%i" %t.id)
	else:
		form = CreateNewList()
	return render(response, "main/create.html", {"form": form})

@login_required(login_url="/login")
def home(response):
	return render(response, "main/home.html", {})


def view(response):
	return render(response, "main/view.html", {})

# def sign_up(response):
# 	if response.method == "POST":
# 		form = RegisterForm(request.POST)
# 	else:
# 		form = RegisterForm() 
# 	return render(response, 'registration/login.html', {"form":form})