from django import forms
from functools import partial
import datetime

from predict.forms import MODEL_CHOICES

class ModelForm(forms.Form):
    model = forms.ChoiceField(label='Model',choices = MODEL_CHOICES,widget=forms.Select(),required=True)
    start_date_str = datetime.date.today().strftime('%Y-%m-%d')
    start_date = forms.CharField(label='',initial=start_date_str,widget=forms.HiddenInput())
    end_date_str = ( datetime.date.today()+datetime.timedelta(days=30) ).strftime('%Y-%m-%d')
    end_date = forms.CharField(label='',initial=end_date_str,widget=forms.HiddenInput())
