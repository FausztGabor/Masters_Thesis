import pandas as pd
from datetime import datetime, timedelta, timezone
from math import sqrt
import statistics as st
from pytz import timezone
import geopy.distance


#stationary = pd.DataFrame({'stationary_lat':[47.4791988], 'stationary_lon' : [19.0562002]})
#



def to_epoch_time(human_time):
    try:
        budapest_tz = timezone('Europe/Budapest')
        datetime_obj = budapest_tz.localize(datetime.strptime(human_time, "%Y-%m-%d %H:%M:%S.%f"))
        temp_time = datetime_obj + timedelta(hours=1)
        return temp_time.timestamp()
    except ValueError:
        print(f"Invalid timestamp: {human_time}") 
        return None
    
def pdr_QAM():
    stationary = (47.4791988,19.0562002) # 64 QAM

    rx = pd.read_csv('Data3\\Logs\\rx.csv', sep= ';')
    tx = pd.read_csv('Data3\\Logs\\tx.csv', sep= ';')

    rx['rx_power'] = rx['rx_power']/2
    rx['rx_noise'] = rx['rx_noise']/2
    tx['tx_power'] = tx['tx_power']/2

    # Merging
    Data = rx.merge(tx, how='inner', on=['Latitude', 'Longitude'])
    Data['Latitude'] = Data['Latitude']*10e-8
    Data['Longitude'] = Data['Longitude']*10e-8
    Data['Latency'] = Data['epochtime_x'] - Data['epochtime_y']
    # Data.drop(columns=['Unnamed: 0_x', 'Unnamed: 0_y'], inplace = True)
    Data.rename(columns={"epochtime_x":"epochtime_rx", "epochtime_y":"epochtime_tx"}, inplace = True)
    dist = []

    for i in range(len(Data)):    
        rx_chord = (Data['Latitude'][i], Data['Longitude'][i])
        distance_meters = geopy.distance.geodesic(stationary, rx_chord).meters
        dist.append(distance_meters)
    Data.insert(8,'Distance to tx',dist)
    snr = Data['rx_power'] - Data['rx_noise']
    Data.insert(6, 'SNR', snr)
    Data.drop(index=0, inplace=True)
    Data.reset_index(inplace=True)
    Data.drop(columns=['index','Unnamed: 0_x', 'Unnamed: 0_y'], inplace = True)
    Data.to_csv('Data3\\Logs\\64QAM_meas.csv', sep=';')
    #print(Data)

    # pdr_rx = rx
    # pdr_tx = tx

    pdr_rx = len(rx.loc[3:])
    pdr_tx = len(tx.loc[(Data['index_y'][0]):(Data['index_y'][len(Data)-1])])
    
    pdr = (pdr_rx/pdr_tx)*100
    
    latency_mean = st.mean(Data['Latency'])
    
    print(f"--------------------------------\n \t 64QAM: \nSent packets: {pdr_tx} \nReceived packets: {pdr_rx} \nPacket delivery ratio: {pdr:.2f}% \nAverage latency: {latency_mean*1000:.3f} ms")
    
def pdr_QPSK():
    stationary = (47.4791692,19.0561941) # 1/2 QPSK

    rx = pd.read_csv('Data2\\Logs\\rx.csv', sep= ';')
    tx = pd.read_csv('Data2\\Logs\\tx.csv', sep= ';')

    rx['rx_power'] = rx['rx_power']/2
    rx['rx_noise'] = rx['rx_noise']/2
    tx['tx_power'] = tx['tx_power']/2

    # Merging
    Data = rx.merge(tx, how='inner', on=['Latitude', 'Longitude'])
    Data['Latitude'] = Data['Latitude']*10e-8
    Data['Longitude'] = Data['Longitude']*10e-8
    Data['Latency'] = Data['epochtime_x'] - Data['epochtime_y']
    # Data.drop(columns=['Unnamed: 0_x', 'Unnamed: 0_y'], inplace = True)
    Data.rename(columns={"epochtime_x":"epochtime_rx", "epochtime_y":"epochtime_tx"}, inplace = True)
    dist = []

    for i in range(len(Data)):    
        rx_chord = (Data['Latitude'][i], Data['Longitude'][i])
        distance_meters = geopy.distance.geodesic(stationary, rx_chord).meters
        dist.append(distance_meters)
    Data.insert(8,'Distance to tx',dist)
    snr = Data['rx_power'] - Data['rx_noise']
    Data.insert(6, 'SNR', snr)
    Data.drop(index=0, inplace=True)
    Data.reset_index(inplace=True)
    Data.drop(columns=['index','Unnamed: 0_x', 'Unnamed: 0_y'], inplace = True)
    Data.to_csv('Data2\\Logs\\1_2QPSK_meas.csv', sep=';')
    #print(Data)

    pdr_rx = len(rx.loc[114:1712])
    pdr_tx = len(tx.loc[1:(len(tx)-1)])

    pdr = (pdr_rx/pdr_tx)*100

    latency_mean = st.mean(Data['Latency'])

    print(f"--------------------------------\n \t 1/2 QPSK: \nSent packets: {pdr_tx} \nReceived packets: {pdr_rx} \nPacket delivery ratio: {pdr:.2f}% \nAverage latency: {latency_mean*1000:.3f} ms")
    
    
    
pdr_QAM()
pdr_QPSK()