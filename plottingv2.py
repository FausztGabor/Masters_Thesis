import pandas as pd
import numpy as np
import folium
from branca.colormap import LinearColormap
import webbrowser
from math import nan


from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans



#CSV INPUT
df_rx = pd.read_csv('Data3\\Logs\\64QAM_meas.csv', sep=';', usecols=[2, 4, 7, 8])

# Color
gradient_rx = LinearColormap(colors=['red', 'orange','yellow','green','cyan', 'blue'], vmin=-100, vmax=-30)

df_rx.columns = ["RX Power","Time", "Latitude", "Longitude"]
df_rx = df_rx.astype(float)
df_rx['RX Power'] = df_rx['RX Power'] / 2
#print(df_rx.isnull().sum())
df_rx = df_rx.dropna(subset=['Latitude', 'Longitude'])   # remove NaN values


####################################
####### Separating the laps ########
####################################
 
start_time = [1705572703.348704, 
              1705572800.419106,
              1705572899.416287    
]

end_time = [1705572798.418714,
            1705572897.415768,
            1705572969.402572             
]

lap_df = [df_rx[(df_rx['Time'] >= start_time[i]) & (df_rx['Time'] <= end_time[i])] for i in range(0,len(start_time))]
#print(lap_df[2])


########################
####### PLOTTING #######
########################

#### Plotting the rectangles

for i in range(0,len(start_time)):
    map_center = [df_rx['Latitude'].mean(), df_rx['Longitude'].mean()]
    map = folium.Map(location=map_center, zoom_start=20)
    color_line = folium.ColorLine(
        positions = lap_df[i][['Latitude', 'Longitude']].values,
        colors=lap_df[i]['RX Power'],
        colormap=gradient_rx,
        weight=2,
        opacity=1,
    ).add_to(map)   
    for index, row in lap_df[i].iterrows():
        color = gradient_rx(row['RX Power'])
        folium.CircleMarker(
            [row['Latitude'], row['Longitude']], radius=2, color=color, fill=True, fill_color=color,
            popup='Latitude: ' + str(row['Latitude']) + ', Longitude: ' + str(row['Longitude']) + ', Rx Power: ' + str(row['RX Power'])+'dBm',
        ).add_to(map)
    map.add_child(folium.LatLngPopup())    
    map.add_child(gradient_rx)
    map.save(f"map_rx_lap_{i}.html")
     
for i in range(0,len(start_time)):
    webbrowser.open(f"map_rx_lap_{i}.html")
map_center = [df_rx['Latitude'].mean(), df_rx['Longitude'].mean()]
map = folium.Map(location=map_center, zoom_start=20)

def plot_customClusters():
    folium.Rectangle(
        bounds=[[47.4790, 19.0560], [47.4792, 19.0563]],
        color = None,
        fill = True,
        fill_color = "blue",
        weight = 10
    ).add_to(map)

    folium.Rectangle(
        bounds=[[47.4790, 19.0560], [47.4784, 19.0563]],
        color = None,
        fill = True,
        fill_color = "green",
        weight = 10
    ).add_to(map)

    folium.Rectangle(
        bounds=[[47.4776, 19.0560], [47.4784, 19.0563]],
        color = None,
        fill = True,
        fill_color = "yellow",
        weight = 10
    ).add_to(map)

    folium.Rectangle(
        bounds=[[47.4776, 19.0563], [47.4782, 19.0574]],
        color = None,
        fill = True,
        fill_color = "red",
        weight = 10
    ).add_to(map)

    folium.Rectangle(
        bounds=[[ 47.4787, 19.0564], [47.4782, 19.0574]],
        color = None,
        fill = True,
        fill_color = "lime",
        weight = 10
    ).add_to(map)

    folium.Rectangle(
        bounds=[[ 47.4792, 19.0563], [47.4787, 19.0570]],
        color = None,
        fill = True,
        fill_color = "aquamarine",
        weight = 10
    ).add_to(map)



folium.ColorLine(
    positions = df_rx[['Latitude', 'Longitude']].values,
    colors=df_rx['RX Power'],
    colormap=gradient_rx,
    weight=2,
    opacity=1,
).add_to(map)   
for index, row in df_rx.iterrows():
    color = gradient_rx(row['RX Power'])
    folium.CircleMarker(
        [row['Latitude'], row['Longitude']], radius=2, color=color, fill=True, fill_color=color,
        popup='Latitude: ' + str(row['Latitude']) + ', Longitude: ' + str(row['Longitude']) + ', Rx Power: ' + str(row['RX Power'])+'dBm',
    ).add_to(map)
map.add_child(folium.LatLngPopup())    
map.add_child(gradient_rx)
map.save(f"map_rx.html")
webbrowser.open(f"map_rx.html")


def kmeans_clustering():
    tx = pd.DataFrame({'tx_lat':[47.4791653], 'tx_lon' : [19.0561952]})
    rx = pd.read_csv('Data1\\MIEV\\adr\\logs\\everythinginIt.csv', sep=';', usecols=[7,8]).astype(float)
    rx_lat = rx['Latitude']
    rx_lon = rx['Longitude']
    coords = np.array([rx_lat, rx_lon]).T
    scaler = StandardScaler().fit(coords)
    scaled_coords = scaler.transform(coords)
    min_samples = 6
    eps = 10
    kmeans = KMeans(n_clusters=2, random_state=0, n_init="auto").fit(coords)



#kmeans_clustering()

plot_customClusters()

