from django.shortcuts import render
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
		return context

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