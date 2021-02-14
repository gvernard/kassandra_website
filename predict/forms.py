from django import forms
from functools import partial
import django.core.exceptions
from decimal import Decimal




class IPForm(forms.Form):
    ip = forms.IntegerField(label='dum',widget=forms.NumberInput(attrs={'type':'range','step': '1'}))
    
    def __init__(self,*args,label,mymin,mymax,**kwargs):
        super(IPForm,self).__init__(*args,**kwargs)
        self.fields['ip'].label = label
        mywidget = forms.NumberInput(attrs={'type':'range','min':mymin,'max':mymax,'step': '1'})
        self.fields['ip'].widget = mywidget


MODEL_CHOICES = (
    ("multi_model_22_12_2020.csv","Kassandra's model 22-12-2020"),
    ("multi_model_19_12_2020.csv","Kassandra's model 19-12-2020"),
)

class PredictorForm(forms.Form):
    country     = forms.CharField(label='Country',initial='Greece',max_length=100)
    region      = forms.CharField(label='Region',max_length=100,required=False)
    rate        = forms.DecimalField(label="Rate",min_value=0.01,max_value=1.0,max_digits=3,decimal_places=2)
    DateInput   = partial(forms.DateInput,{'class': 'datepicker'})
    start_date  = forms.DateField(label='Start date',input_formats=['%Y-%m-%d'],widget=DateInput())
    end_date    = forms.DateField(label='End date',input_formats=['%Y-%m-%d'],widget=DateInput())
    model_field = forms.ChoiceField(label='Model',choices = MODEL_CHOICES,widget=forms.Select(),required=True)
