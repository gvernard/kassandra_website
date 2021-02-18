from django import forms
from functools import partial

from predict.forms import MODEL_CHOICES

class ModelForm(forms.Form):
    model = forms.ChoiceField(label='Model',choices = MODEL_CHOICES,widget=forms.Select(),required=True)
