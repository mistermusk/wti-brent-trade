import eia
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

api_key = "265d1f2178aaab3ceec3d364d9cc1d11";
api = eia.API(api_key);

wti_daily = pd.DataFrame(api.data_by_series(series='PET.RWTC.D'));
brent_daily = pd.DataFrame(api.data_by_series(series='PET.RBRTE.D'));


def data_correction(input):
    return input[:9];
def convert_to_datetime(input):
    return datetime.datetime.strptime(input, "%Y %m%d").date();

wti_daily.index = wti_daily.index.map(data_correction);
wti_daily.index = wti_daily.index.map(convert_to_datetime);
wti_daily.index = pd.to_datetime(wti_daily.index);
wti_daily.columns = ['PET.RWTC.D'];

brent_daily.index = brent_daily.index.map(data_correction);
brent_daily.index = brent_daily.index.map(convert_to_datetime);
brent_daily.index = pd.to_datetime(brent_daily.index);
brent_daily.columns = ['PET.RBRTE.D'];


df = pd.concat([wti_daily, brent_daily], axis=1, join='outer');

df = df['2018-01-01':].fillna(method='ffill');
df['Spread'] = df['PET.RBRTE.D'] - df['PET.RWTC.D'];
df['5-MA'] = df['Spread'].rolling(5).mean();
df['10-MA'] = df['Spread'].rolling(10).mean();
df.drop(['PET.RWTC.D', 'PET.RBRTE.D'], axis=1).plot();
plt.show();



df.to_csv("df.csv");

print(df);
