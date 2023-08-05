"""
forecast.py - Forecast 
Usage:
    forecast.py [options]
    forecast.py -h | --help

Options:
    -h --help             Show this message.
    --output_folder=OUT   Output folder for the data and reports to be saved.
    --num_days=INT        Number of days that the model will forecast in the future
"""

from __future__ import print_function
import re
import os
import sys
import math
import docopt
import pandas as pd
from math import sqrt
from time import strftime
from datetime import timedelta
import matplotlib.pyplot as plt
from dateutil.parser import parse
from pmdarima.arima import auto_arima
from datetime import datetime, date, time 
from sklearn.metrics import mean_squared_error
from covidify.config import PERC_SPLIT, FIG_SIZE

font = {'weight' : 'bold',
        'size'   : 22}

plt.rc('font', **font)
plt.style.use('ggplot')
pd.options.display.max_rows = 999

args = docopt.docopt(__doc__)
out = args['--output_folder']
days_in_future = int(args['--num_days'])
           
# file paths
image_dir =  os.path.join(out,'reports', 'images')
trend_file  = 'trend_{}.csv'.format(datetime.date(datetime.now()))
forecast_file  = 'forecast_{}.csv'.format(datetime.date(datetime.now())) # For saving forecasts
data_dir  = os.path.join(out, 'data', str(datetime.date(datetime.now())))
trend_df = pd.read_csv(os.path.join(data_dir, trend_file)).reset_index(drop=True)


# For forecasting (use all data for training)
train_start = datetime.strptime(trend_df.date.min(), "%Y-%m-%d")
train_end = datetime.strptime(trend_df.date.max(), "%Y-%m-%d")
forecast_start = datetime.strptime(trend_df.date.max(), "%Y-%m-%d") + timedelta(days=1)
forecast_end = datetime.strptime(trend_df.date.max(), "%Y-%m-%d") + timedelta(days=days_in_future+1) # Extra day because of one day lag

train_period = [d.strftime('%Y-%m-%d') for d in pd.date_range(train_start, train_end)]
forecast_period = [d.strftime('%Y-%m-%d') for d in pd.date_range(forecast_start, forecast_end)]


if not os.path.exists(image_dir):
    print('Creating reports folder...')
    os.system('mkdir -p ' + image_dir)


def plot_forecast(tmp_df, train, index_forecast, forecast, confint):
    '''
    Plot the values of train and test, the predictions from ARIMA and the shadowing
    for the confidence interval.
    
    '''

    # For shadowing
    lower_series = pd.Series(confint[:, 0], index=index_forecast)
    upper_series = pd.Series(confint[:, 1], index=index_forecast)
    
    print('... saving graph')
    fig, ax = plt.subplots(figsize=FIG_SIZE)
    plt.title('ARIMA - Prediction for cumalitive case counts {} days in the future'.format(days_in_future))    
    plt.plot(tmp_df.cumulative_cases, label='Train',marker='o')
    plt.plot(tmp_df.pred, label='Forecast', marker='o')
    tmp_df.groupby('date')[['']].sum().plot(ax=ax)
    plt.fill_between(index_forecast, 
                     upper_series, 
                     lower_series, 
                     color='k', alpha=.1)
    plt.ylabel('Infections')
    plt.xlabel('Date')
    fig.legend().set_visible(True)
    fig = ax.get_figure()
    fig.savefig(os.path.join(image_dir, 'cumulative_forecasts.png'))


def forecast(tmp_df, train, index_forecast, days_in_future):
    
    # Fit model with training data
    model = auto_arima(train, trace=False, error_action='ignore', suppress_warnings=True)
    model_fit = model.fit(train)
        
    forecast, confint = model_fit.predict(n_periods=len(index_forecast), return_conf_int=True)

    forecast_df = pd.concat([tmp_df, pd.DataFrame(forecast, index = index_forecast, columns=['pred'])], axis=1, sort=False)
    date_range = [d.strftime('%Y-%m-%d') for d in pd.date_range(train_start, forecast_end)]
    forecast_df['date'] = pd.Series(date_range).astype(str)
    forecast_df[''] = None # Dates get messed up, so need to use pandas plotting
        
    # Save Model and file
    print('... saving file:', forecast_file)
    forecast_df.to_csv(os.path.join(data_dir, forecast_file))
        
    plot_forecast(forecast_df, train, index_forecast, forecast, confint)
    
if __name__ == '__main__':
    print('Training forecasting model...')

    train = trend_df[trend_df.date.isin(train_period)].cumulative_cases
    index_forecast = [x for x in range(train.index[-1]+1, train.index[-1] + days_in_future+1)]
    forecast(trend_df, train, index_forecast, days_in_future)
