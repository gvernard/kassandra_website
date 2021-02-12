from kassandra_predictor import make_prediction,get_latest_hist,MY_IPS



print(len(MY_IPS))

dates,new,q25,q75 = make_prediction('Spain__',0.06,1,'2020-12-11','2020-12-20',[0]*len(MY_IPS))
print(q25)
print(new)
print(q75)

date,ips = get_latest_hist('Spain__')
print(date)
print(ips)
