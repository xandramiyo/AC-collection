from django.forms import ModelForm
from .models import Note, Home

class NoteForm(ModelForm):
	class Meta:
		model = Note
		fields = '__all__'

class HomeForm(ModelForm):
	class Meta:
		model = Home
		fields = '__all__'