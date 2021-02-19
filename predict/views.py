from django.shortcuts import render
from django.http import JsonResponse
from django.forms import BaseFormSet
from django.forms import formset_factory
import pandas as pd
import json
import os
import datetime

from .forms import IPForm,PredictorForm

from .kassandra_predictor.kassandra_predictor import make_prediction
from .kassandra_predictor.kassandra_predictor import get_latest_hist
from .kassandra_predictor.kassandra_predictor import match_model_coeffs_to_colors


IP_MAX_VALUES = {
    'C1_School closing': 3,
    'C2_Workplace closing': 3,
    'C3_Cancel public events': 2,
    'C4_Restrictions on gatherings': 4,
    'C5_Close public transport': 2,
    'C6_Stay at home requirements': 3,
    'C7_Restrictions on internal movement': 2,
    'C8_International travel controls': 4,
    'H1_Public information campaigns': 2,
    'H2_Testing policy': 3,
    'H3_Contact tracing': 2,
    'H6_Facial Coverings': 4
}
MY_IPS = list(IP_MAX_VALUES.keys())

MY_HIST_IPS = [None]*len(MY_IPS)

class BaseIPSFormSet(BaseFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['label'] = MY_IPS[index]
        kwargs['myval'] = MY_HIST_IPS[index]
        kwargs['mymin'] = 0
        kwargs['mymax'] = IP_MAX_VALUES[MY_IPS[index]]
        return kwargs

# Create your views here.
def predict(request):
    init_dict = {
        "country": request.GET.get("country","Greece"),
        "rate": request.GET.get("rate",0.03),
        "start_date": request.GET.get("start_date",datetime.date.today()),
        "end_date": request.GET.get("end_date",datetime.date.today()+datetime.timedelta(days=30)),
        "model_field": request.GET.get("model_field","multi_model_22_12_2020.csv"),
    }
    form1 = PredictorForm(initial=init_dict)
    latest_date,latest_ips = get_latest_hist(init_dict["country"]+"__")
    for i in range(0,len(latest_ips)):
        MY_HIST_IPS[i] = latest_ips[i]
    formset = formset_factory(IPForm,extra=len(MY_IPS),formset=BaseIPSFormSet)
    year = datetime.datetime.now().year
    return render(request,"predict.html",{'form1':form1,'formset':formset,'year':year,'latest_ips_date':latest_date,'my_latest':MY_HIST_IPS})


def get_latest_ips(request):
    country = str(request.GET.get('country',None))
    region  = str(request.GET.get('region',None))
    if region == 'None':
        geo = country + '__'
    else:
        geo = country + '__' + region
    latest_date,latest_ips = get_latest_hist(geo)
    response = {
        "geo": geo,
        "date": latest_date,
        "ips": latest_ips
    }
    return JsonResponse(response)






def get_model_colors(request):
    country = str(request.GET.get('country',None))
    region  = str(request.GET.get('region',None))
    if region == 'None':
        geo = country + '__'
    else:
        geo = country + '__' + region
    model  = str(request.GET.get('model_field',None))    
    colors = match_model_coeffs_to_colors(geo,model)
    response = {
        "geo": geo,
        "colors": colors
    }
    return JsonResponse(response)


def get_countries_and_regions(request):
    this_path = os.path.dirname(__file__)
    latest_df = pd.read_csv(this_path+'/kassandra_predictor/data/latest_df.csv',parse_dates=['Date'],encoding="ISO-8859-1",dtype={"GeoID": str},error_bad_lines=False)
    geos = latest_df.GeoID.unique().tolist()

    countries = []
    for i in range(0,len(geos)):
        strlist = geos[i].split('__')
        countries.append(strlist[0])
    countries = list(set(countries))
    countries.sort()

    regions = {}
    for i in range(0,len(countries)):
        regions[countries[i]] = []
    
    for i in range(0,len(geos)):
        strlist = geos[i].split('__')
        if strlist[1]:
            regions[strlist[0]].append(strlist[1])

    for i in range(0,len(countries)):
        regions[countries[i]].sort()
            
    response = { "countries": countries, "regions": regions }
    return JsonResponse(response)



def test_predictor(request):
    country = str(request.GET.get('country',None))
    region  = str(request.GET.get('region',None))
    if region == 'None':
        geo = country + '__'
    else:
        geo = country + '__' + region
    #K     = float(request.GET.get('K',None))
    K = 1
    rate  = float(request.GET.get('rate',None))
    start_date = str(request.GET.get('start_date'))
    end_date = str(request.GET.get('end_date'))
    model  = str(request.GET.get('model_field',None))

    IP_vector = []
    for i in range(0,len(MY_IPS)):
        IP_vector.append(request.GET.get('form-'+str(i)+'-ip_text'))
        
    dates,newCases,quant25,quant75 = make_prediction(geo,rate,K,start_date,end_date,IP_vector,model)
    data_newCases = []
    data_quant25  = []
    data_quant75  = []
    for i in range(0,len(dates)):
        point1 = {}
        point1["x"] = dates[i]
        point1["y"] = newCases[i]
        data_newCases.append(point1)
        point2 = {}
        point2["x"] = dates[i]
        point2["y"] = quant25[i]
        data_quant25.append(point2)
        point3 = {}
        point3["x"] = dates[i]
        point3["y"] = quant75[i]
        data_quant75.append(point3)
        
    response = {
        "geo": geo,
        "newCases": data_newCases,
        "quant25": data_quant25,
        "quant75": data_quant75,
    }
        
    return JsonResponse(response)
