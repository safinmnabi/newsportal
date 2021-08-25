from django.db import models

class Users(models.Model):
	fullname=models.CharField(max_length=255)
	email=models.CharField(max_length=255)
	password=models.CharField(max_length=255)
	token=models.TextField(null=True)
	expire_token=models.CharField(max_length=55, null=True)
	status=models.IntegerField(default=0)

	def __str__(self):
		return self.fullname

class Settings(models.Model):
	country=models.TextField(null=True)
	source=models.TextField(null=True)
	keyword=models.TextField(null=True)
	userid=models.CharField(max_length=255)

	def __str__(self):
		return self.country

		