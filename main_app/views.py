from django.shortcuts import render, redirect
from django.http import HttpResponse

import os
import uuid
import boto3
import requests

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Villager, Home, Note, Photo
from .forms import NoteForm, HomeForm

url = 'https://acnhapi.com/v1/villagers/'
response = requests.get(url)
data = response.json()

# Create your views here.
def home(request):
	return render(request, 'home.html')

def about(request):
	return render(request, 'about.html')

class VillagerList(ListView):
	model = Villager
	template_name = 'villagers/villager_list.html'

class VillagerDetail(DetailView):
	model = Villager
	template_name = 'villagers/villager_details.html'
	def get_context_data(self, **kwargs):
		context = super(VillagerDetail, self).get_context_data(**kwargs)
		context['villager_list'] = Villager.objects.all()
		context['home_list'] = Home.objects.all()
		context['note_form'] = NoteForm()
		return context
	
	def post(self, request, *args, **kwargs):
		home_id = int(request.POST['home_id'])
		villager_id = kwargs['pk']
		Villager.objects.get(id=villager_id).homes.add(home_id)
		return redirect('villager_details', pk=villager_id)

class VillagerCreate(CreateView):
	model = Villager
	fields = ['name']
	# succes_url = '/villagers'

	def form_valid(self, form):
		#1: find name of the villager in the form
		name = form.cleaned_data['name']
		#2: iterate over data and check if a villager object's name matches the form's name
		for villager_name in data:
			if name.lower() == data[villager_name]['name']['name-USen'].lower():
			#3: if there is a match, a photo object will be created
				villager_photo = data[villager_name]['image_uri']
				Villager.villager_img = villager_photo
				villager_personality = data[villager_name]['personality']
				Villager.personality = villager_personality
				villager_species = data[villager_name]['species']
				Villager.species = villager_species
				villager_birthday = data[villager_name]['birthday-string']
				Villager.birthday = villager_birthday
				villager_catchphrase = data[villager_name]['catch-phrase']
				new_villager = Villager.objects.create(name=name, personality=villager_personality, species=villager_species, birthday=villager_birthday, catchphrase=villager_catchphrase, villager_img=villager_photo)
				new_villager.save()
		return redirect('villagers_index')
				

class VillagerUpdate(UpdateView):
	model = Villager
	fields = ['name', 'personality', 'species', 'birthday', 'catchphrase']
	succes_url = '/villagers/villager_id'

class VillagerDelete(DeleteView):
	model = Villager
	success_url = '/villagers'

def add_note(request, villager_id):
	form = NoteForm(request.POST)
	print(request.POST)
	if form.is_valid():
		new_note = form.save(commit=False)
		new_note.villager_id = villager_id
		new_note.save()
	return redirect('villager_details', villager_id)

class NoteDelete(DeleteView):
	model = Note
	sucess_url = '/villagers/villager_id'

class HomeList(ListView):
	model = Home
	def get_context_data(self, **kwargs):
		home_form = HomeForm()
		context = super(HomeList, self).get_context_data(**kwargs)
		context['home_form'] = home_form
		return context

class HomeCreate(CreateView):
	model = Home
	fields = '__all__'

class HomeUpdate(UpdateView):
	model = Home
	fields = '__all__'

class HomeDelete(DeleteView):
	model = Home
	success_url = '/homes'

def assoc_home(request, villager_id, home_id):
	Villager.objects.get(id=villager_id).homes.add(home_id)
	return redirect('villager_details', villager_id=villager_id)

def diss_home(request, villager_id, home_id):
	Villager.objects.get(id=villager_id).homes.remove(home_id)
	return redirect('villager_details', villager_id)

def add_photo(request, pk):
	photo_file = request.FILES.get('photo-file', None)
	if photo_file:
		s3 = boto3.client('s3')
		key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
		try:
			bucket = os.environ['S3_BUCKET']
			s3.upload_fileobj(photo_file, bucket, key)
			url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
			Photo.objects.create(url=url, villager=Villager.objects.get(id=pk))
		except Exception as e:
			print('An error occurred uploading file to S3')
			print(e)
	return redirect('villager_details', pk=pk)