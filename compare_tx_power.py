import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import geopy.distance
import matplotlib as plt
import matplotlib.pyplot as plt
from statistics import mean
import seaborn as sns
import matplotlib.pyplot as plt

tx_0 = pd.read_csv('Data1\\Suzuki\\tx_0dBm.csv', sep=';',usecols=[3, 4]).astype(float)
tx_0 = (mean(tx_0['latitude'])/(10e6), mean(tx_0['longitude'])/(10e6))


tx_10 = pd.read_csv('Data1\\Suzuki\\tx_10dBm.csv', sep=';',usecols=[3, 4]).astype(float)
tx_10 = (mean(tx_10['latitude'])/(10e6), mean(tx_10['longitude'])/(10e6))

tx_20 = pd.read_csv('Data1\\Suzuki\\tx_20dBm.csv', sep=';',usecols=[3, 4]).astype(float)
tx_20 = (mean(tx_20['latitude'])/(10e6), mean(tx_20['longitude'])/(10e6))

tx_33 = pd.read_csv('Data1\\Suzuki\\tx_33dBm.csv', sep=';',usecols=[3, 4]).astype(float)
tx_33 = (mean(tx_33['latitude'])/(10e6), mean(tx_33['longitude'])/(10e6))


df_0 = pd.read_csv('Data1\\MIEV\\ADR\\logs\\everythinginIt_0dBm .csv', sep=';').astype(float)
df_10 = pd.read_csv('Data1\\MIEV\\ADR\\logs\\everythinginIt_10dBm .csv', sep=';').astype(float)
df_20 = pd.read_csv('Data1\\MIEV\\ADR\\logs\\everythinginIt_20dBm .csv', sep=';').astype(float)
df_33 = pd.read_csv('Data1\\MIEV\\ADR\\logs\\everythinginIt_33dBm .csv', sep=';').astype(float)

Latency = pd.DataFrame({'0 dBm':df_0['LATENCY'], '10 dBm':df_10['LATENCY'],'20 dBm':df_20['LATENCY'],'33 dBm':df_33['LATENCY'],})*1000
Latency = Latency.dropna()

sns.boxplot(data=Latency)
plt.title('Dobozdiagram a késleltetés idejéről a küldő jel erősségének függvényében')
plt.ylabel('Késleltetés [ms]')
plt.xlabel('Küldő jel erőssége')
plt.show()

dist, rx = [], []

for i in range(len(df_0)):    
    rx_chord = (df_0['Latitude'][i], df_0['Longitude'][i])
    distance_meters = geopy.distance.geodesic(tx_0, rx_chord).meters
    dist.append(distance_meters)
    
    rx_power = (df_0['rx_power'][i])/2
    rx.append(rx_power)
df_0_new = pd.DataFrame({
    'RX Power': rx,
    'Distance to tx': dist
})

for i in range(len(df_10)):    
    rx_chord = (df_10['Latitude'][i], df_10['Longitude'][i])
    distance_meters = geopy.distance.geodesic(tx_10, rx_chord).meters
    dist.append(distance_meters)
    
    rx_power = (df_10['rx_power'][i])/2
    rx.append(rx_power)
df_10_new = pd.DataFrame({
    'RX Power': rx,
    'Distance to tx': dist
})

for i in range(len(df_20)):    
    rx_chord = (df_20['Latitude'][i], df_20['Longitude'][i])
    distance_meters = geopy.distance.geodesic(tx_20, rx_chord).meters
    dist.append(distance_meters)
    
    rx_power = (df_20['rx_power'][i])/2
    rx.append(rx_power)
df_20_new = pd.DataFrame({
    'RX Power': rx,
    'Distance to tx': dist
})

for i in range(len(df_33)):    
    rx_chord = (df_33['Latitude'][i], df_33['Longitude'][i])
    distance_meters = geopy.distance.geodesic(tx_33, rx_chord).meters
    dist.append(distance_meters)
    
    rx_power = (df_33['rx_power'][i])/2
    rx.append(rx_power)
df_33_new = pd.DataFrame({
    'RX Power': rx,
    'Distance to tx': dist
})


df_0_new['tag'] = '0dBm'
df_10_new['tag'] = '10dBm'
df_20_new['tag'] = '20dBm'
df_33_new['tag'] = '33dBm'



def plot_rx_power():
    plt.figure() 
    
    df_0_new.sort_values('Distance to tx', inplace=True)
    df_10_new.sort_values('Distance to tx', inplace=True)
    df_20_new.sort_values('Distance to tx', inplace=True)
    df_33_new.sort_values('Distance to tx', inplace=True)
    
    scaler = StandardScaler()
    
    X = df_0_new['Distance to tx'].values.reshape(-1, 1)
    X_scaled = scaler.fit_transform(X)
    X_poly = PolynomialFeatures(degree=4).fit_transform(X_scaled)
    y = df_0_new['RX Power']
    model1 = LinearRegression().fit(X_poly, y)
    plt.plot(X, model1.predict(X_poly), color='blue', label='0 dBm', linestyle = 'solid')
    
    X = df_10_new['Distance to tx'].values.reshape(-1, 1)
    X_scaled = scaler.fit_transform(X)
    X_poly = PolynomialFeatures(degree=4).fit_transform(X_scaled)
    y = df_10_new['RX Power']
    model2 = LinearRegression().fit(X_poly, y)
    plt.plot(X, model2.predict(X_poly), color='orange', label='10 dBm', linestyle = 'solid')
    
    X = df_20_new['Distance to tx'].values.reshape(-1, 1)
    X_scaled = scaler.fit_transform(X)
    X_poly = PolynomialFeatures(degree=4).fit_transform(X_scaled)
    y = df_20_new['RX Power']
    model3 = LinearRegression().fit(X_poly, y)
    plt.plot(X, model3.predict(X_poly), color='green', label='20 dBm', linestyle = 'solid')
    
    X = df_33_new['Distance to tx'].values.reshape(-1, 1)
    X_scaled = scaler.fit_transform(X)
    X_poly = PolynomialFeatures(degree=4).fit_transform(X_scaled)
    y = df_33_new['RX Power']
    model4 = LinearRegression().fit(X_poly, y)
    plt.plot(X, model4.predict(X_poly), color='red', label='33 dBm', linestyle = 'solid')  

    plt.xlabel('Távolság a küldőtől [m]')
    plt.ylabel('Fogadott jel erőssége [dBm]')
    plt.title('A fogadott jel erőssége a küldőtől való távolság függvényében')
    plt.grid(True)
    plt.legend()

    plt.show()

plot_rx_power()


## PDR calc


