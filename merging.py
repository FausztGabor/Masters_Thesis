import pandas as pd
from datetime import datetime, timedelta, timezone
from math import sqrt
from pytz import timezone
import time



# Read CSV files
df1 = pd.read_csv('Data1\\MIEV\\adr\\adr_20dBm.csv')


budapest_tz = timezone('Europe/Budapest')
delta = timedelta(hours=1)


############################################
### Convert ADR timestamp to epoch time, ###
###  Rename RX time column to epochtime  ###
############################################


def to_epoch_time(human_time):
    try:
        budapest_tz = timezone('Europe/Budapest')
        datetime_obj = budapest_tz.localize(datetime.strptime(human_time, "%Y-%m-%d %H:%M:%S.%f"))
        temp_time = datetime_obj + timedelta(hours=1)
        return temp_time.timestamp()
    except ValueError:
        print(f"Invalid timestamp: {human_time}") 
        return None



for i in range(df1.shape[0]):
    df1.loc[i, 'Time'] = to_epoch_time(df1.loc[i, 'Time'])
    #print(df1['Time'][i])
df1 = df1.rename(columns={'Time': 'epochtime'})



# Calculate latitude and longitude differences
latdiff = []
londiff = []
sqrta = []

dflogs = df1[['epochtime', 'Latitude', 'Longitude']]
for i in range(dflogs.shape[0]):
    if i == 0:
        latdiff.append(0)
        londiff.append(0)
        sqrta.append(0)
    else:
        latdiff.append((dflogs['Latitude'][i] - dflogs['Latitude'][i-1])*10**8)
        londiff.append((dflogs['Longitude'][i] - dflogs['Longitude'][i-1])*10**8)
        sqrta.append(sqrt(latdiff[i]**2 + londiff[i]**2))

# Add new columns to dflogs
dflogs.insert(3, '-', '')
dflogs.insert(4, 'Lat_diff', latdiff)
dflogs.insert(5, '--', '')
dflogs.insert(6, 'Lon_diff', londiff)
dflogs.insert(7,'---','')
dflogs.insert(8,'mean', sqrta)

# Save to CSV
dflogs.to_csv('Data1\\MIEV\\adr\\logs\\20dBm_logs.csv', sep=';')


# print("Wait for 3 sec.")
# time.sleep(3)


df1 = pd.read_csv('Data1\\MIEV\\adr\\logs\\20dBm_logs.csv', sep= ';')
df2 = pd.read_csv('Data1\\MIEV\\rx\\rx_20dBm.csv', sep=';')
df3 = pd.read_csv('Data1\\Suzuki\\tx_20dBm.csv', sep=';')



# df4 = pd.read_csv('Data1\\MIEV\\adr\\logs\\mergedData.csv', sep = ';', usecols = [2, 6])

# df1['epochtime'] = df1.loc[:, 'epochtime'].astype(float)
# df2['epochtime'] = df2.loc[:, 'epochtime'].astype(float)
# df3['epochtime'] = df2.loc[:, 'epochtime'].astype(float)

# df1['epochtime'] = pd.to_numeric(df1['epochtime'], errors='coerce')  # Handle conversion errors
# df2['epochtime'] = pd.to_numeric(df2['epochtime'], errors='coerce')
# df3['epochtime'] = df2['epochtime'].astype(str)

df1.sort_values(by='epochtime', inplace=True)
df2.sort_values(by='epochtime', inplace=True)
df3.sort_values(by='epochtime', inplace=True)
# df4.sort_values(by='Time', inplace=True)


df3['tx_power'] = df3['tx_power']/2
df3['TX EPOCH TIME'] = df3['epochtime']

# df4.rename(columns={'Time': 'epochtime'}, inplace=True)
#print(df1['epochtime'].dtype)


# Add latlong coordinates from ADR.pcap to RX dataframe
#position = pd.merge_asof(df2, df1, left_on='epochtime', right_on='epochtime', by='epochtime', direction='nearest')
position = pd.merge_asof(df2, df1, on='epochtime', direction='nearest')

# Add tx epochtime to calculate latency
latency = pd.merge_asof(position, df3, on='epochtime', direction='backward')
latency['LATENCY'] = latency['epochtime'] - latency['TX EPOCH TIME'] 
#latency['Latency'] = latency['epochtime'] - latency['epochtime']

## Add Cluster Tags

#everythinginIt = pd.merge_asof(latency, df4, on = 'epochtime', direction = 'nearest')
everythinginIt = latency

everythinginIt.to_csv('Data1\\MIEV\\adr\\logs\\everythinginIt_20dBm .csv', sep=';')



#df3 = df1.set_index('adrTime').reindex(df2.set_index('epochtime').index, method='nearest').reset_index()