from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name='home'),
	path('about/', views.about, name='about'),
	path('villagers/', views.VillagerList.as_view(), name='villager_index'),
	#using CBV, need to use pk not id
	path('villagers/<int:pk>/', views.VillagerDetail.as_view(), name='villager_details'),
	path('villagers/create/', views.VillagerCreate.as_view(), name='villagers_create'),
]