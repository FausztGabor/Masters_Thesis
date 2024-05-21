
import pandas as pd
import numpy as np
import geopy.distance
import matplotlib.pyplot as plt
from math import sin, cos, sqrt, atan2, radians
from scipy.optimize import curve_fit


blue_boundaries = pd.DataFrame({'Latitude':[47.4790, 47.4792], 'Longitude' :[19.0560, 19.0563]})

green_boundaries = pd.DataFrame({'Latitude':[47.4784, 47.4790], 'Longitude' :[19.0560, 19.0563]})

yellow_boundaries = pd.DataFrame({'Latitude':[47.4776, 47.4784], 'Longitude' :[19.0560, 19.0563]})

red1_boundaries = pd.DataFrame({'Latitude':[47.4776, 47.4782], 'Longitude' :[19.0563, 19.0574]})

# red2_boundaries = pd.DataFrame({'Latitude':[47.4776, 47.4782], 'Longitude' :[19.0564, 19.0574]})

lime_boundaries = pd.DataFrame({'Latitude':[47.4782, 47.4787], 'Longitude' :[19.0564, 19.0574]})

aquamarine_boundaries = pd.DataFrame({'Latitude':[47.4787, 47.4792], 'Longitude' :[19.0563, 19.0570]})

#### Dataset ####

data = pd.read_csv('Data1\\MIEV\\adr\\logs\\everythinginIt_33dBm .csv', sep=';', usecols=[4, 6, 8, 9])
data.columns = ["RX Power","Time", "Latitude", "Longitude"]
data = data.astype(float)
data['RX Power'] = data['RX Power'] / 2
data = data.dropna(subset=['Latitude', 'Longitude'])   # remove NaN values

latency = pd.read_csv('Data1\\MIEV\\adr\\logs\\everythinginIt.csv', sep=';', usecols=[2,21])
print(latency)
data = pd.merge_asof(data, latency, left_on='Time', right_on='epochtime', direction='nearest')


blue, green, yellow, red, lime, aquamarine = [], [], [], [], [], []
lat, lon, dlat, dlon, dist = [], [], [], [], []

# tx = pd.DataFrame({'Latitude':[47.4791653], 'Longitude' :[19.0561952]})
tx = (47.4791653, 19.0561952)


#### Clusters ####
for i in range(len(data)):    
    rx_chord = (data['Latitude'][i], data['Longitude'][i])
    distance_meters = geopy.distance.geodesic(tx, rx_chord).meters
    dist.append(distance_meters)
data.insert(4, 'Distance to tx', dist)

for i in range(len(data)):
    lat, lon = data.loc[i, 'Latitude'], data.loc[i, 'Longitude']
    
    if blue_boundaries['Latitude'][0] <= lat <= blue_boundaries['Latitude'][1] and \
       blue_boundaries['Longitude'][0] <= lon <= blue_boundaries['Longitude'][1]:
        blue.append(data.loc[i])
    elif green_boundaries['Latitude'][0] <= lat <= green_boundaries['Latitude'][1] and \
         green_boundaries['Longitude'][0] <= lon <= green_boundaries['Longitude'][1]:
        green.append(data.loc[i])
    elif yellow_boundaries['Latitude'][0] <= lat <= yellow_boundaries['Latitude'][1] and \
         yellow_boundaries['Longitude'][0] <= lon <= yellow_boundaries['Longitude'][1]:
        yellow.append(data.loc[i])
    elif red1_boundaries['Latitude'][0] <= lat <= red1_boundaries['Latitude'][1] and \
         red1_boundaries['Longitude'][0] <= lon <= red1_boundaries['Longitude'][1]:
        red.append(data.loc[i])
    # elif red2_boundaries['Latitude'][0] <= lat <= red2_boundaries['Latitude'][1] and \
    #      red2_boundaries['Longitude'][0] <= lon <= red2_boundaries['Longitude'][1]:
    #     red.append(data.loc[i])
    elif lime_boundaries['Latitude'][0] <= lat <= lime_boundaries['Latitude'][1] and \
         lime_boundaries['Longitude'][0] <= lon <= lime_boundaries['Longitude'][1]:
        lime.append(data.loc[i])
    elif aquamarine_boundaries['Latitude'][0] <= lat <= aquamarine_boundaries['Latitude'][1] and \
         aquamarine_boundaries['Longitude'][0] <= lon <= aquamarine_boundaries['Longitude'][1]:
        aquamarine.append(data.loc[i])

#print
blue = pd.DataFrame(blue)
blue['Tag'] = 'blue'
green = pd.DataFrame(green)    
green['Tag'] = 'green'   
yellow = pd.DataFrame(yellow)    
yellow['Tag'] = 'yellow' 
red = pd.DataFrame(red) 
red['Tag'] = 'red'
lime = pd.DataFrame(lime)
lime['Tag'] = 'lime'        
aquamarine = pd.DataFrame(aquamarine)
aquamarine['Tag'] = 'aquamarine'

def print_to_csv():             
    blue.to_csv('Data1\\MIEV\\adr\\logs\\blue.csv', sep=';') 
    green.to_csv('Data1\\MIEV\\adr\\logs\\green.csv', sep=';')     
    yellow.to_csv('Data1\\MIEV\\adr\\logs\\yellow.csv', sep=';')
    red.to_csv('Data1\\MIEV\\adr\\logs\\red.csv', sep=';')
    lime.to_csv('Data1\\MIEV\\adr\\logs\\lime.csv', sep=';')
    aquamarine.to_csv('Data1\\MIEV\\adr\\logs\\aquamarine.csv', sep=';')

frames = [blue, green, yellow, red, lime, aquamarine]
mergedData = pd.concat(frames)
mergedData.to_csv('Data1\\MIEV\\adr\\logs\\mergedData.csv', sep=';')


######## Plotting #######

# ax = mergedData.plot()
#mergedData.sort_values('Distance to tx', inplace=True)
def scatterplot(scatterData):
    fig, ax = plt.subplots()
    ax.scatter(x = scatterData['Distance to tx'], y = scatterData['RX Power'], c=scatterData['Tag'], linewidth=0.2)
    plt.title("Received Signal Strength depending on the distance from the transmitter")
    ax.set_xlabel("Distance to transmitter")
    ax.set_ylabel("RX Power")
    ax.grid()
    ax.text( 
        3.2,
        55,
        "The colour of the markers indicates the clusters",
    )
    ax.set(xlim=(0, 175),ylim=(-100, 0))
    plt.show()

  
def plot_cluster(cluster, id):    
    plt.scatter(x = cluster['Distance to tx'], y = cluster['RX Power'], c=cluster['Tag'], linewidth=0.2)  
    cluster.sort_values('Distance to tx', inplace=True)
    plt.plot(cluster['Distance to tx'], cluster['RX Power'], c = cluster['Tag'][id], linewidth=1)
    plt.title(f"Received Signal Strength in cluster {cluster['Tag']} depending on the distance from the transmitter")
    plt.xlabel("Distance to transmitter")
    plt.ylabel("RX Power")
    plt.grid(True)
    plt.xlim=(cluster['Distance to tx'] - 10, cluster['Distance to tx'] + 10),
    plt.ylim=(cluster['RX Power'] - 10, cluster['RX Power'] + 10)
    plt.show()


def boxplot():
    plt.figure(figsize=(15, 6))
    plt.boxplot([blue['RX Power'], green['RX Power'],yellow['RX Power'], red['RX Power'], lime['RX Power'], aquamarine['RX Power']], vert=True, patch_artist=True)
    plt.xticks([1, 2, 3, 4 ,5 ,6], ['Blue', 'Green', 'Yellow', 'Red', 'Lime', 'Aquamarine'])
    plt.ylabel('RX Power')
    plt.grid(True)
    plt.title('Boxplots of RX Power from the clusters')
    plt.show()
    

def plot_all_clusters():
    plot_cluster(blue, 1)
    plot_cluster(green, 5)
    plot_cluster(yellow, 20)
    plot_cluster(red, 44)
    plot_cluster(lime, 58)
    plot_cluster(aquamarine, 72)

# def plot_latency(latency, id):
#     plt.scatter(x = latency['Distance to tx'], y = latency['LATENCY'], c=latency['Tag'], linewidth=0.2)
#     #plt.plot(latency['Distance to tx'], latency['LATENCY'], c = latency['Tag'][id], linewidth=1)
#     plt.title(f"Received Signal Strength in cluster {latency['Tag']} depending on the distance from the transmitter")
#     plt.xlabel("Distance to transmitter")
#     plt.ylabel("RX Power")
#     plt.grid(True)
#     plt.xlim=(latency['Distance to tx'] - 10, latency['Distance to tx'] + 10),
#     #plt.ylim=(latency['LATENCY'] -1 , latency['LATENCY'] + 1)
#     plt.show()

def plot_latency():
    blue.drop(blue.index[:5], inplace=True)
    green.drop(green.index[:3], inplace=True)
    plt.figure(figsize=(15, 6))
    plt.boxplot([blue['LATENCY'], green['LATENCY'],yellow['LATENCY'], red['LATENCY'], lime['LATENCY'], aquamarine['LATENCY']], vert=True, patch_artist=True)
    plt.xticks([1, 2, 3, 4 ,5 ,6], ['Blue', 'Green', 'Yellow', 'Red', 'Lime', 'Aquamarine'])
    plt.ylabel('Latency')
    plt.grid(True)
    plt.title('Latency from the clusters')
    plt.show()

plot_latency()

plot_all_clusters()
boxplot()
