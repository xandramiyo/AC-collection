from django.db import models
from django.urls import reverse

# Create your models here.

class Villager(models.Model):
	name = models.CharField(max_length=100)
	personality = models.CharField(max_length=100)
	species = models.CharField(max_length=100)
	birthday = models.CharField(max_length=15)
	catchprase = models.CharField(max_length=50)

	def __str__(self):
		return f'{self.name} ({self.id})'
	
	def get_absolute_url(self):
		return reverse('villager_details', kwargs={'pk': self.id})