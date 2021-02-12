import pandas as pd
import json
import os

this_path = os.path.dirname(os.path.realpath(__file__))
print(this_path)
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

print(regions)
