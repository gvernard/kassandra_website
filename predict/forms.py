from django import forms
from functools import partial
import django.core.exceptions
from decimal import Decimal
import datetime




class IPForm(forms.Form):
    ip_slider = forms.IntegerField(label='dum',widget=forms.NumberInput(attrs={'type':'range','step': '1'}))
    ip_text   = forms.IntegerField(label='',widget=forms.NumberInput(attrs={'type':'text','readonly':True}))
    
    def __init__(self,*args,label,mymin,mymax,myval,**kwargs):
        super(IPForm,self).__init__(*args,**kwargs)
        self.fields['ip_slider'].label = label
        slider_widget = forms.NumberInput(attrs={'type':'range','min':mymin,'max':mymax,'value':myval,'step': '1'})
        self.fields['ip_slider'].widget = slider_widget
        text_widget = forms.NumberInput(attrs={'type':'text','value':int(myval),'readonly':True})
        self.fields['ip_text'].widget = text_widget
        


MODEL_CHOICES = (
    ("multi_model_22_12_2020.csv","Kassandra 22-12-2020"),
    ("multi_model_19_12_2020.csv","Kassandra 19-12-2020"),
)

class PredictorForm(forms.Form):
    country     = forms.CharField(label='Country',max_length=100)
    region      = forms.CharField(label='Region',max_length=100,required=False)
    rate        = forms.DecimalField(label="Rate",min_value=0.01,max_value=1.0,max_digits=3,decimal_places=2)
    DateInput   = partial(forms.DateInput,{'class': 'datepicker'})
    start_date  = forms.DateField(label='Start date',input_formats=['%Y-%m-%d'],widget=DateInput())
    end_date    = forms.DateField(label='End date',input_formats=['%Y-%m-%d'],widget=DateInput())
    model_field = forms.ChoiceField(label='Model',choices = MODEL_CHOICES,widget=forms.Select(),required=True)
