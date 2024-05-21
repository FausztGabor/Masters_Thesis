import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from sklearn import datasets
from sklearn.cluster import KMeans


rx = pd.read_csv('Data3\\Logs\\rx.csv', sep= ';')
tx = pd.read_csv('Data3\\Logs\\tx.csv', sep= ';')

df = pd.read_csv('Data3\\Logs\\64QAM_meas.csv', sep= ';')




######################
### Tx timestamps ####
######################


o = 0.95 #offset
##
blue_ts_start = [
    1705572703.348704-o,
    1705572794.403941-o,
    1705572895.414809-o
]

blue_ts_end = [
    1705572707.360614,
    1705572811.403124,
    1705572909.403659
]

green_ts_start = [
    1705572708.364664-o,
    1705572812.402683-o,
    1705572910.415487-o,
]

green_ts_end = [
    1705572722.402729,
    1705572824.402699,
    1705572922.415465,
]

yellow_ts_start = [
    1705572723.402317-o,
    1705572825.418089-o,
    1705572923.404307-o,
]

yellow_ts_end = [
    1705572746.402282,
    1705572843.415838,
    1705572939.415756
]

red_ts_start = [
    1705572747.414599-o,
    1705572844.415187-o,
    1705572940.416196-o
]

red_ts_end = [
    1705572765.415588,
    1705572865.415997,
    1705572961.402941
]

lime_ts_start = [
    1705572766.417117-o,
    1705572866.416118-o,
    1705572962.402629-o
]

lime_ts_end = [
    1705572779.415735,
    1705572880.415474,
    1705572969.402572
]

aquamarine_ts_start = [
    1705572780.415773-o,
    1705572881.417319-o
]

aquamarine_ts_end = [
    1705572793.395654,
    1705572894.417715
]

### Counters

tx_counter = {
    'blue' : 0,
    'green' : 0,
    'yellow' : 0,
    'red' : 0,
    'lime' : 0,
    'aquamarine' : 0
}

rx_counter = {
    'blue' : 0,
    'green' : 0,
    'yellow' : 0,
    'red' : 0,
    'lime' : 0,
    'aquamarine' : 0
}

#blue, green, yellow, red, lime, aquamarine = 0, 0, 0, 0, 0, 0


for i in range(len(tx)):
    ts = tx.loc[i,'epochtime'].astype(float)
    for j in range(len(blue_ts_start)):
        if blue_ts_start[j] <= ts <= blue_ts_end[j]:
            tx_counter['blue'] += 1
    for j in range(len(green_ts_start)):
        if green_ts_start[j] <= ts <= green_ts_end[j]:
            tx_counter['green'] += 1
    for j in range(len(yellow_ts_start)):
        if yellow_ts_start[j] <= ts <= yellow_ts_end[j]:
            tx_counter['yellow'] += 1
    for j in range(len(red_ts_start)):
        if red_ts_start[j] <= ts <= red_ts_end[j]:
            tx_counter['red'] += 1
    for j in range(len(lime_ts_start)):
        if lime_ts_start[j] <= ts <= lime_ts_end[j]:
            tx_counter['lime'] += 1
    for j in range(len(aquamarine_ts_start)):
        if aquamarine_ts_start[j] <= ts <= aquamarine_ts_end[j]:
            tx_counter['aquamarine'] += 1
            
for i in range(len(rx)):
    if rx.loc[i, 'Tag'] == 'blue':
        rx_counter['blue'] += 1
    if rx.loc[i, 'Tag'] == 'green':
        rx_counter['green'] += 1   
    if rx.loc[i, 'Tag'] == 'yellow':
        rx_counter['yellow'] += 1   
    if rx.loc[i, 'Tag'] == 'red':
        rx_counter['red'] += 1   
    if rx.loc[i, 'Tag'] == 'lime':
        rx_counter['lime'] += 1
    if rx.loc[i, 'Tag'] == 'aquamarine':
        rx_counter['aquamarine'] += 1
    

print(f' Sent packets: {tx_counter}') 
print(f' Received packets: {rx_counter}')


blue_pdr = rx_counter['blue'] / tx_counter['blue']
green_pdr = rx_counter['green'] / tx_counter['green']
yellow_pdr = rx_counter['yellow'] / tx_counter['yellow']
red_pdr = rx_counter['red'] / tx_counter['red']
lime_pdr = rx_counter['lime'] / tx_counter['lime'] 
aquamarine_pdr = rx_counter['aquamarine'] / tx_counter['aquamarine']
sum1 = rx_counter['blue'] + rx_counter['green'] + rx_counter['yellow'] + rx_counter['red'] + rx_counter['lime'] + rx_counter['aquamarine']
sum2 = tx_counter['blue'] + tx_counter['green'] + tx_counter['yellow'] + tx_counter['red'] + tx_counter['lime'] + tx_counter['aquamarine']
all = sum1 / sum2
all = blue_pdr*green_pdr*yellow_pdr*red_pdr*
                
pdr = {
    blue_pdr,
    green_pdr,
    yellow_pdr,
    red_pdr,
    lime_pdr,
    aquamarine_pdr,
    all
}        
        
print(f'Blue: {blue_pdr*100}, Green: {green_pdr*100}, Yellow: {yellow_pdr*100}, Red: {red_pdr*100}, Lime: {lime_pdr*100}, Aquamarine: {aquamarine_pdr*100}, All: {all*100}')






### K-means clusters ###

