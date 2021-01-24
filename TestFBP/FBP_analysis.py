#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 16:29:34 2020

@author: lfiorentini
"""

import pandas as pd
from fbprophet import Prophet
from fbprophet.plot import add_changepoints_to_plot
import time
import argparse
from datetime import timedelta, datetime
import json

"""
READING PARAMETERS

"""

with open('parameters.json', 'r') as json_file:
    param = json.load(json_file)
    json_file.close()

"""
PARSING OPTIONS

"""

parser = argparse.ArgumentParser()
parser.add_argument("-i", help="input file", default = param['input_file'],
                    type = str)
parser.add_argument("-d", help="days to predict",
                    default = param['days_to_predict'], type = int)
input_file = str(parser.parse_args().i)
days2predict = int(parser.parse_args().d)

"""
LOADING DATA AND DEFINING LOCKDOWN PERIOD
"""

Data = pd.read_csv(input_file)

if param['lockdown']:
    sdate = datetime.strptime(param["lockdown_start"], "%Y-%m-%d").date()
    edate = datetime.strptime(param["lockdown_end"], "%Y-%m-%d").date()
    
    delta = edate - sdate       # as timedelta
    
    conf_list = []
    for i in range(delta.days + 1):
        conf_list.append(sdate + timedelta(days = i))
        
    extra_holiday = pd.DataFrame({
      'holiday': 'lockdown',
      'ds': pd.to_datetime(conf_list),
      'lower_window': 0,
      'upper_window': 1,
    })
else:
    extra_holiday = False

#changepoints=['2020-03-17', '2020-05-11', '2020-07-28', '2008-09-14']
start_time = time.time()
pro = Prophet(growth = param['growth'],
              #default = 'linear'
              yearly_seasonality = param['yearly_seasonality'],
              #default = True
              weekly_seasonality = param['weekly_seasonality'],
              #default = True
              daily_seasonality = param['daily_seasonality'],
              #default = True
              holidays = extra_holiday,
              #default = None
              changepoint_range = param['changepoint_range'],
              #default = 0.8
              changepoint_prior_scale = param['changepoint_prior_scale']
              #default = 0.5
              )
pro.add_country_holidays(country_name = param['country_name'])
pro.fit(Data)
end_time = time.time()
print("Fitting time:", end_time - start_time)

future = pro.make_future_dataframe(periods = days2predict)
forecast = pro.predict(future)
fig1 = pro.plot(forecast)
a = add_changepoints_to_plot(fig1.gca(), pro, forecast)
fig1.savefig(param['prevision_plot'])
fig2 = pro.plot_components(forecast)
fig2.savefig(param['components_plot'])