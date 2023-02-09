from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Villager, Home, Note
from .forms import HomeForm

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
	print(villager_id)
	return redirect('villager_details', villager_id)

