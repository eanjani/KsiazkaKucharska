from django import forms
from .models import Skladniki
from .models import Przepisy
from django.forms import ModelForm
from django.forms.models import modelformset_factory

class SkladnikForm(forms.ModelForm):
	
	class Meta:
		model = Skladniki
		fields = ('nazwa','miara','ilosc')

		
class PrzepisForm(forms.ModelForm):
	
	class Meta:
		model = Przepisy
		fields = ('nazwa','kategoria','ilosc_porcji', 'przygotowanie')#'fotografia', 'fotografia_url')