from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
class Course(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course', null=True)
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=2000)

	def __str__(self):
		s = str(self.name) + "," + str(self.description)
		return str(s)

class Student(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	sex = models.BooleanField(default=False)
	DOB = models.DateField(default=date.today)
	address = models.CharField(max_length=200)

	def __str__(self):
		s = str(self.name) + "," + str(self.sex) + "," + str(self.DOB) + "," + str(self.address)
		return str(s)