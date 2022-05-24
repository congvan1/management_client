from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('home/', views.home, name='home'),
	path('view/', views.view, name='views'),
	path('list_student=<int:id>', views.index, name='index'),
	path('create/', views.create, name='create'),
	path('register/', views.register, name='register')
]