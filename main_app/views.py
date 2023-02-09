from django.shortcuts import render, redirect

import requests

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Villager, Home, Note
from .forms import NoteForm, HomeForm

# Create your views here.
def home(request):
	url = 'https://acnhapi.com/v1/villagers/'
	response = requests.get(url)
	data = response.json()
	context = {
		'data' : data
	}

	return render(request, 'home.html', context)

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
		return context
	
	def post(self, request, *args, **kwargs):
		home_id = int(request.POST['home_id'])
		villager_id = kwargs['pk']
		Villager.objects.get(id=villager_id).homes.add(home_id)
		return redirect('villager_details', pk=villager_id)

class VillagerCreate(CreateView):
	model = Villager
	fields = ['name', 'personality', 'species', 'birthday', 'catchphrase']
	succes_url= '/villagers'

class VillagerUpdate(UpdateView):
	model = Villager
	fields = ['name', 'personality', 'species', 'birthday', 'catchphrase']
	succes_url= '/villagers/villager_id'

class VillagerDelete(DeleteView):
	model = Villager
	success_url = '/villagers'

def add_note(request, villager_id):
	form = NoteForm()
	if form.is_valid():
		new_note = form.save(commit=False)
		print(villager_id)
		new_note.villager_id = villager_id
		new_note.save()
	return redirect('villager_details', villager_id)


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
