from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import Villager

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
		print(context)
		return context

class VillagerCreate(CreateView):
	model = Villager
	fields = '__all__'
	succes_url= '/villagers'

class VillagerUpdate(UpdateView):
	model = Villager
	fields = '__all__'
	succes_url= '/villagers/villager_id'