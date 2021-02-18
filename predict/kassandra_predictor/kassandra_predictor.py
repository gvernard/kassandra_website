import sys
import os
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.cm

MY_IPS = ['C1_School closing',
          'C2_Workplace closing',
          'C3_Cancel public events',
          'C4_Restrictions on gatherings',
          'C5_Close public transport',
          'C6_Stay at home requirements',
          'C7_Restrictions on internal movement',
          'C8_International travel controls',
          'H1_Public information campaigns',
          'H2_Testing policy',
          'H3_Contact tracing',
          'H6_Facial Coverings']


def match_model_coeffs_to_colors(geo,model_file):
    this_path = os.path.dirname(__file__)
    model_df = pd.read_csv(this_path+'/models/'+model_file,encoding="ISO-8859-1",dtype={"Name": str},error_bad_lines=False)
    coeffs = abs( model_df[model_df['GeoID'] == geo].drop(columns=['GeoID']).values )
    means = np.mean(coeffs,axis=0)
    mean_max = means.max()
    cmap = matplotlib.cm.get_cmap('Greens')
    colors = []
    for i in range(0,len(means)):
        colors.append( matplotlib.colors.to_hex(cmap(means[i]/(1.2*mean_max))) )
    return colors


def make_prediction(geo,rate,K,start_date,end_date,IPS_vector,model_file):
    this_path = os.path.dirname(__file__)
    kas_pred = KassandraPredictor(this_path+"/",model_file,geo,rate,K)

    forecast_df = kas_pred.predict(start_date,end_date,IPS_vector)

    dates = [d.strftime('%Y-%m-%d') for d in pd.date_range(start=start_date,end=end_date)]
    newCases = forecast_df["PredictedDailyNewCases"].tolist()
    quant25  = forecast_df["PredictedDailyQuantile_25"].tolist()
    quant75  = forecast_df["PredictedDailyQuantile_75"].tolist()
    newCases = [round(num) for num in newCases]
    quant25  = [round(num) for num in quant25]
    quant75  = [round(num) for num in quant75]
    
    return dates,newCases,quant25,quant75


def get_latest_hist(geo):
    this_path = os.path.dirname(__file__)
    hist_df = pd.read_csv(this_path+'/data/latest_df.csv',parse_dates=['Date'],encoding="ISO-8859-1",dtype={"GeoID": str},error_bad_lines=False)
    hist_df = hist_df[hist_df.GeoID == geo]
    IPS_vector = hist_df[MY_IPS].loc[hist_df.Date.idxmax()].values.tolist()
    latest_hist_date = hist_df.loc[hist_df.Date.idxmax()].at['Date'].date().strftime('%Y-%m-%d')
    return latest_hist_date,IPS_vector
    

class KassandraPredictor:
    project_root = '.'
    coeffs = []
    latest_new_cases = 0.0
    hist_df = pd.DataFrame(index=[0],columns=[0])
    ips_df = pd.DataFrame(index=[0],columns=[0])

    Llog = 4
    K = 0.5
    M = 200
    rate = 0.03

    
    h = [0.012346,
         0.024691,
         0.037037,
         0.049383,
         0.061728,
         0.074074,
         0.08642,
         0.098765,
         0.11111,
         0.098765,
         0.08642,
         0.074074,
         0.061728,
         0.049383,
         0.037037,
         0.024691,
         0.012346
    ]
    
    def __init__(self,project_root,model_file,geo,rate,K):
        self.rate = rate
        self.K = K
        
        self.project_root = project_root
        model_df = pd.read_csv(project_root+'models/'+model_file,encoding="ISO-8859-1",dtype={"Name": str},error_bad_lines=False)
        self.coeffs = model_df[model_df['GeoID'] == geo].drop(columns=['GeoID']).values.tolist()
            
        hist_df = pd.read_csv(project_root+'data/latest_df.csv',parse_dates=['Date'],encoding="ISO-8859-1",dtype={"GeoID": str},error_bad_lines=False)
        self.hist_df = hist_df[hist_df.GeoID == geo]
        last_index = self.hist_df.Date.idxmax()
        self.latest_hist_date = self.hist_df.loc[last_index].at['Date']
        tmp = self.hist_df['NewCases'].iloc[-7:last_index].values
        self.latest_new_cases = np.mean(tmp[np.nonzero(tmp)])

        
    def predict(self,start_date_str,end_date_str,IPS_vector):
        start_date = pd.to_datetime(start_date_str,format='%Y-%m-%d')
        end_date   = pd.to_datetime(end_date_str,format='%Y-%m-%d')

        if start_date > self.latest_hist_date:
            pred_start_date = self.latest_hist_date
        else:
            pred_start_date = start_date
            last_index = self.hist_df[self.hist_df.Date <= pred_start_date].Date.idxmax()
            tmp = self.hist_df['NewCases'].iloc[-7:last_index].values
            self.latest_new_cases = np.mean(tmp[np.nonzero(tmp)])


        IPS_vector = list(map(int,IPS_vector))
        if IPS_vector is None:
            IPS_vector = self.hist_df[MY_IPS].loc[self.hist_df.Date.idxmax()]




            
        n_days = (end_date - pred_start_date).days + 1
        
        # Set a dictionary of lists that will contain the output
        forecast = {"Date": [],"PredictedDailyNewCases": [],"PredictedDailyQuantile_25": [],"PredictedDailyQuantile_75": []}
            
        dates = [d.strftime('%Y-%m-%d') for d in pd.date_range(start=pred_start_date,end=end_date)]
        tmp_df = {'Date': dates}
        for j in range(0,len(MY_IPS)):
            tmp_df[MY_IPS[j]] = [IPS_vector[j]] * len(dates)
        ips_df = pd.DataFrame(tmp_df)
        ips_df['Date'] = pd.to_datetime(ips_df['Date'])

        # slice the input required to make a prediction by Date and IPS
        latest_data = ips_df[(ips_df.Date >= pred_start_date) & (ips_df.Date <= end_date)]
        latest_data = latest_data[MY_IPS].values
            
        # Here call the prediction model
        pred_new_cases,pred_25,pred_75 = self.predict_per_country_multi(n_days,latest_data)                
            
        geo_start_date = pred_start_date
        #for i,pred in enumerate(pred_new_cases):
        for i in range(0,len(pred_new_cases)):
            current_date = geo_start_date + pd.offsets.Day(i)
            forecast["Date"].append(current_date)
            forecast["PredictedDailyNewCases"].append(pred_new_cases[i])
            forecast["PredictedDailyQuantile_25"].append(pred_25[i])
            forecast["PredictedDailyQuantile_75"].append(pred_75[i])

        # Convert dictionary to DataFrame
        forecast_df = pd.DataFrame.from_dict(forecast)

        # Impose positivity
        forecast_df['PredictedDailyNewCases'] = forecast_df['PredictedDailyNewCases'].clip(lower=0)
        forecast_df['PredictedDailyQuantile_25'] = forecast_df['PredictedDailyQuantile_25'].clip(lower=0)
        forecast_df['PredictedDailyQuantile_75'] = forecast_df['PredictedDailyQuantile_75'].clip(lower=0)
        
        # Return only the requested predictions
        return forecast_df[(forecast_df.Date >= start_date) & (forecast_df.Date <= end_date)]



    def Psi_multi(self,n_days,latest_ips):
        N_IPS = len(MY_IPS)
        mat = np.zeros((n_days,N_IPS+1))
        mat[:,0] = 1
        latest_ips = latest_ips/4.0
        last_line = np.array([latest_ips[-1,:]])
        for k in range(0,len(self.h)):
            latest_ips = np.concatenate((latest_ips,last_line),axis=0)
        for k in range(0,N_IPS):
            dum = np.convolve(self.h,latest_ips[:,k])
            mat[:,k+1] = dum[-n_days-len(self.h):-len(self.h)]
        return mat

    def predict_per_country_multi(self,n_days,latest_ips):
        n_models = len(self.coeffs)
        if n_models > 0:
            model_predictions = np.zeros((n_models,n_days))
            for k in range(0,n_models):
            #for k in range(0,1):
                a_hat = self.coeffs[k]
                
                psi = self.Psi_multi(n_days,latest_ips)
                
                z_hat = psi.dot(a_hat)

                y_hat = np.zeros(n_days)
                y_hat[0] = (self.Llog + self.latest_new_cases)*np.exp(z_hat[0]) - self.Llog
                for i in range(1,len(y_hat)):
                    if i > self.K:
                        y_hat[i] = (self.Llog + y_hat[i-1])*np.exp(z_hat[i] - self.rate*(i-self.K)/self.M) - self.Llog
                    else:
                        y_hat[i] = (self.Llog + y_hat[i-1])*np.exp(z_hat[i]) - self.Llog
                model_predictions[k,:] = y_hat

            pred_new_cases = [0] * n_days
            pred_25 = [0] * n_days
            pred_75 = [0] * n_days
            for d in range(0,n_days):
                preds = np.sort(model_predictions[:,d])
                preds = preds[5:-5]
                quants = np.percentile(preds,[25,50,75],interpolation='linear')

                pred_new_cases[d] = quants[1]
                pred_25[d] = quants[0]
                pred_75[d] = quants[2]
        else :
            pred_new_cases = [0] * n_days
            pred_25 = [0] * n_days
            pred_75 = [0] * n_days

        return pred_new_cases,pred_25,pred_75
