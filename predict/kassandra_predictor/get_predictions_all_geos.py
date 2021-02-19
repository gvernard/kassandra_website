import os
import pandas as pd
import kassandra_predictor
import datetime
import numpy as np
from kassandra_predictor import make_prediction,get_latest_hist

K = 0.5
rate = 0.03
start_date_str = datetime.date.today().strftime('%Y-%m-%d')
end_date_str = ( datetime.date.today()+datetime.timedelta(days=30) ).strftime('%Y-%m-%d')
MODEL_CHOICES = (
    ("multi_model_22_12_2020.csv","Kassandra 22-12-2020"),
    ("multi_model_19_12_2020.csv","Kassandra 19-12-2020"),
)



# Get countries
this_path = os.path.dirname(__file__)
oxford_df = pd.read_csv(this_path+'data/latest_df.csv',parse_dates=['Date'],encoding="ISO-8859-1",dtype={"GeoID": str},error_bad_lines=False)
geos = oxford_df.GeoID.unique()

new_geos = []
for geo in geos:
    dum = geo.split('__')
    new_geos.append(dum[0])
countries = list(set(new_geos))
countries.sort()

#excluded = ['Greenland','Solomon Islands','Tajikistan']
#countries = [c for c in countries if c not in excluded]

column_names = ["CountryName","Date","PredictedDailyNewCases","PredictedDailyQuantile25","PredictedDailyQuantile75"]
df = pd.DataFrame(columns=column_names)


for model in MODEL_CHOICES:
    model_file = model[0]
    print('################ Model: '+model_file)

        
    for country in countries:
        geo = country+'__'
        latest_date,IP_vector = get_latest_hist(geo)
        print(country,IP_vector)
        dates,newCases,quant25,quant75 = make_prediction(geo,rate,K,start_date_str,end_date_str,IP_vector,model_file)
        for i in range(0,len(dates)):
            new_row = {'CountryName':country,'Date':dates[i],'PredictedDailyNewCases':newCases[i],'PredictedDailyQuantile25':quant25[i],'PredictedDailyQuantile75':quant75[i]}
            df = df.append(new_row,ignore_index=True)

    dum = model_file.split('.')
    out_name = '../../home/latest_predictor_run/all_countries_'+dum[0]+'.csv'
    df.to_csv(out_name,index=False)       
