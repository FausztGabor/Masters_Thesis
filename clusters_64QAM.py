import pandas as pd
import numpy as np
import folium
from branca.colormap import LinearColormap
import webbrowser
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
import geopy.distance
import matplotlib as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.pyplot as plt
from statistics import mean
from scipy import stats
from scipy.integrate import quad

tx = pd.DataFrame({'tx_lat':[47.4791988], 'tx_lon' : [19.0562002]})
rx = pd.read_csv('Data3\\Logs\\64QAM_meas.csv', sep=';').astype(float)
#rssi = rx['rx_power']
#rx['rx_power'] = rx['rx_power']/2
rx_lat = rx['Latitude']
rx_lon = rx['Longitude']
rx_power = rx['rx_power'].values

# asd = pd.read_csv('Data1\\MIEV\\adr\\logs\\mergedData.csv', sep=';', usecols=[2, 5])
# asd.sort_values(by='Time', inplace=True)
distance = rx['Distance to tx']

gradient_rx = LinearColormap(colors=['blue','turquoise','green','yellow','orange','red','darkred'], vmin=-100, vmax=-30)


# coords = np.array([distance, rx_power]).T

coords = rx['Distance to tx'].values.reshape(-1, 1)
scaler = StandardScaler().fit(coords)
scaled_coords = scaler.transform(coords)

min_samples = 6
eps = 10
cluster_numbers = 5
kmeans = KMeans(n_clusters = cluster_numbers, random_state=0, n_init="auto").fit(coords)




#############################################
############ Custom Clusters ################
#############################################

red1_cluster = pd.DataFrame({'Latitude':[47.4785, 47.47925], 'Longitude' :[19.0560, 19.0565]})
red2_cluster = pd.DataFrame({'Latitude':[47.47865, 47.47925], 'Longitude' :[19.0565, 19.0570]})
yellow_cluster = pd.DataFrame({'Latitude':[47.47765, 47.4785], 'Longitude' :[19.0560, 19.0563]})
blue1_cluster = pd.DataFrame({'Latitude':[47.47755, 47.47765], 'Longitude' :[19.0560, 19.0563]})
blue2_cluster = pd.DataFrame({'Latitude':[47.47755, 47.4782], 'Longitude' :[19.0563, 19.0574]})
green_cluster = pd.DataFrame({'Latitude':[47.4782, 47.47865], 'Longitude' :[19.0565, 19.0574]})

def plot_customClusters(m):
    folium.Rectangle(
        bounds=[[red1_cluster['Latitude'][0], red1_cluster['Longitude'][0]], 
                [red1_cluster['Latitude'][1], red1_cluster['Longitude'][1]]],
        color = None,
        fill = True,
        fill_color = "red",
        weight = 10
    ).add_to(m)
    
    folium.Rectangle(
        bounds=[[red2_cluster['Latitude'][0], red2_cluster['Longitude'][0]], 
                [red2_cluster['Latitude'][1], red2_cluster['Longitude'][1]]],
        color = None,
        fill = True,
        fill_color = "red",
        weight = 10
    ).add_to(m)

    folium.Rectangle(
        bounds=[[yellow_cluster['Latitude'][0], yellow_cluster['Longitude'][0]], 
                [yellow_cluster['Latitude'][1], yellow_cluster['Longitude'][1]]],
        color = None,
        fill = True,
        fill_color = "yellow",
        weight = 10
    ).add_to(m)

    folium.Rectangle(
        bounds=[[blue1_cluster['Latitude'][0], blue1_cluster['Longitude'][0]], 
                [blue1_cluster['Latitude'][1], blue1_cluster['Longitude'][1]]],
        color = None,
        fill = True,
        fill_color = "blue",
        weight = 10
    ).add_to(m)

    folium.Rectangle(
        bounds=[[blue2_cluster['Latitude'][0], blue2_cluster['Longitude'][0]], 
                [blue2_cluster['Latitude'][1], blue2_cluster['Longitude'][1]]],
        color = None,
        fill = True,
        fill_color = "blue",
        weight = 10
    ).add_to(m)

    folium.Rectangle(
        bounds=[[green_cluster['Latitude'][0], green_cluster['Longitude'][0]], 
                [green_cluster['Latitude'][1], green_cluster['Longitude'][1]]],
        color = None,
        fill = True,
        fill_color = "green",
        weight = 10
    ).add_to(m)
    # folium.ColorLine(
    # positions = rx[['Latitude', 'Longitude']].values,
    # colors=rx['rx_power'],
    # colormap=gradient_rx,
    # weight=2,
    # opacity=1,
    # ).add_to(m)   
    for index, row in rx.iterrows():
        color = gradient_rx(row['rx_power'])
        folium.CircleMarker(
            [row['Latitude'], row['Longitude']], radius=2, color=color, fill=True, fill_color=color,
            popup='Latitude: ' + str(row['Latitude']) + ', Longitude: ' + str(row['Longitude']) + ', Rx Power: ' + str(row['rx_power'])+'dBm',
        ).add_to(m)
m = folium.Map(location=[red1_cluster['Latitude'].mean(), red1_cluster['Longitude'].mean()], zoom_start=20)
m.add_child(gradient_rx)

map_title = "64 QAM"
title_html = f'<h1 style="position:absolute;z-index:100000;left:20vw" >{map_title}</h1>'
m.get_root().html.add_child(folium.Element(title_html))

plot_customClusters(m)
m.save("custom_clusters.html")
webbrowser.open("custom_clusters.html")


#color_map = cm.get_cmap('rainbow', len(np.unique(kmeans.labels_)))
color_map = plt.colormaps.get_cmap('rainbow')(np.linspace(0, 1, len(np.unique(kmeans.labels_))))

def plot_to_osm():
    for lat, lon, rx_power, cluster_label in zip(rx_lat, rx_lon, rx['rx_power'], kmeans.labels_):
        color = colors.rgb2hex(color_map[cluster_label])
        folium.CircleMarker(
            [lat, lon], 
            radius=2, 
            color=color, 
            fill=True, 
            fill_color=color, 
            popup='Latitude: ' + str(lat) + ', Longitude: ' + str(lon) + ', Rx Power: ' + str(rx_power)+'dBm' + ', Cluster ID: ' + str(cluster_label)
        ).add_to(map)
    map.add_child(folium.LatLngPopup())    
    map.save('clustered_map.html')
    webbrowser.open(f"clustered_map.html")


green, yellow, red, blue = [], [], [], [],
lat, lon, dist = [], [], [] 


# for i in range(len(rx)):    
#     rx_chord = (rx['Latitude'][i], rx['Longitude'][i])
#     tx = [47.4791653, 19.0561952]
#     distance_meters = geopy.distance.geodesic(tx, rx_chord).meters
#     dist.append(distance_meters)
# rx.insert(22, 'Distance to tx', dist)

for i in range(len(rx)):
    lat, lon = rx.loc[i, 'Latitude'], rx.loc[i, 'Longitude']
    
    if red1_cluster['Latitude'][0] <= lat < red1_cluster['Latitude'][1] and \
       red1_cluster['Longitude'][0] <= lon < red1_cluster['Longitude'][1]:
        red.append(rx.loc[i])
    elif red2_cluster['Latitude'][0] <= lat < red2_cluster['Latitude'][1] and \
        red2_cluster['Longitude'][0] <= lon < red2_cluster['Longitude'][1]:
        red.append(rx.loc[i])
    elif yellow_cluster['Latitude'][0] <= lat < yellow_cluster['Latitude'][1] and \
         yellow_cluster['Longitude'][0] <= lon < yellow_cluster['Longitude'][1]:
        yellow.append(rx.loc[i])
    elif blue1_cluster['Latitude'][0] <= lat < blue1_cluster['Latitude'][1] and \
         blue1_cluster['Longitude'][0] <= lon < blue1_cluster['Longitude'][1]:
        blue.append(rx.loc[i])
    elif blue2_cluster['Latitude'][0] <= lat < blue2_cluster['Latitude'][1] and \
         blue2_cluster['Longitude'][0] <= lon < blue2_cluster['Longitude'][1]:
        blue.append(rx.loc[i])
    elif green_cluster['Latitude'][0] <= lat <= green_cluster['Latitude'][1] and \
         green_cluster['Longitude'][0] <= lon <= green_cluster['Longitude'][1]:
        green.append(rx.loc[i])
    


red = pd.DataFrame(red) 
red['Color'] = ['red' for _ in range(len(red))]
red['Cluster ID'] = ['0' for _ in range(len(red))]
red.sort_values('Distance to tx', inplace = True)

yellow = pd.DataFrame(yellow)    
yellow['Color'] = ['gold' for _ in range(len(yellow))]
yellow['Cluster ID'] = ['1' for _ in range(len(yellow))]
yellow.sort_values('Distance to tx', inplace = True)

green = pd.DataFrame(green)    
green['Color'] = ['green' for _ in range(len(green))]
green['Cluster ID'] = ['2' for _ in range(len(green))]
green.sort_values('Distance to tx', inplace = True)

blue = pd.DataFrame(blue)
blue['Color'] = ['blue' for _ in range(len(blue))]
blue['Cluster ID'] = ['3' for _ in range(len(blue))]
blue.sort_values('Distance to tx', inplace = True)

def KMEANS_create_df_to_matlab():
    df = pd.DataFrame({
        'EpochTime': rx['epochtime'],
        'Latitude': rx_lat,
        'Longitude': rx_lon,
        'Rx Power': rx['rx_power'],
        'Distance': distance
    })

    df['Cluster ID'] = kmeans.labels_
    df['Color'] = [colors.rgb2hex(color_map[label]) for label in kmeans.labels_]
    df.to_csv('Data1\\MIEV\\adr\\logs\\clustered_data.csv', index=False, sep=';')

frames = [green, yellow, red, blue]
mergedData = pd.concat(frames)
mergedData['Cluster ID'] = mergedData['Cluster ID'].astype(int)

def CUSTOM_create_df_to_matlab():
    df = pd.DataFrame({
        'EpochTime': mergedData['epochtime_rx'],
        'Latitude': mergedData['Latitude'],
        'Longitude': mergedData['Longitude'],
        'Rx Power': mergedData['rx_power'],
        'Distance': mergedData['Distance to tx'],
        'Cluster ID': mergedData['Cluster ID'],
        'Color': mergedData['Color']
    })

    df.to_csv('Data3\\Logs\\custom_clustered_data.csv', index=False, sep=';')

CUSTOM_create_df_to_matlab()

from_matlab = pd.read_csv('Data3\\Logs\\propModellData.csv')

from_matlab.columns = ["Epochtime", "Latitude", "Longitude", "RX Power", "Distance to TX","Cluster ID", "RT Matlab", "FSPL Matlab","Delta"]
#from_matlab['RT Matlab'] = from_matlab['RT Matlab'].replace([np.inf, -np.inf], -100)
from_matlab = from_matlab.replace([np.inf, -np.inf], np.nan)
from_matlab = from_matlab.dropna(subset=['RT Matlab'])
from_matlab['Cluster ID'] = from_matlab['Cluster ID'].astype(int)
from_matlab['Color'] = from_matlab['Cluster ID'].map(mergedData.set_index('Cluster ID')['Color'].to_dict())
#from_matlab["Color"] = [colors.rgb2hex(color_map[label]) for label in kmeans.labels_]
from_matlab['Color'] = mergedData['Color']

clusters = {}
# for index, row in from_matlab.iterrows():
#     cluster_id = row["Cluster ID"]
#     cluster_colors = mergedData.loc[mergedData["Cluster ID"] == cluster_id, "Color"].values[0]
#     clusters[cluster_id] = cluster_colors

# print(cluster_colors)

def get_color(row):
    cluster_id = row["Cluster ID"]
    return mergedData.loc[mergedData["Cluster ID"] == cluster_id, "Color"].values[0]

from_matlab["Color"] = from_matlab.apply(get_color, axis=1)
cluster_colors = from_matlab.set_index('Cluster ID')['Color'].to_dict()


for cluster_id in from_matlab['Cluster ID'].unique():
    clusters[cluster_id] = from_matlab[from_matlab['Cluster ID'] == cluster_id]

def plot_separate_CUSTOM_clusters():  
    for cluster_id, cluster_data in clusters.items():
        plt.figure()  
        color = cluster_colors[cluster_id]  
        plt.scatter(x = cluster_data['Distance to TX'], y = cluster_data['RX Power'], c = color, linewidth=0.4, marker=".", label='Real measurement')
        plt.scatter(x = cluster_data['Distance to TX'], y = cluster_data['RT Matlab'], c = color, linewidth=0.2, marker="^", label='RT model')
        # plt.scatter(x = cluster_data['Distance to TX'], y = cluster_data['FSPL Matlab'], c = color, linewidth=0.2, marker="s", label='FSPL model')
        
        cluster_data.sort_values('Distance to TX', inplace=True)
        plt.plot(cluster_data['Distance to TX'], cluster_data['RX Power'], linewidth=0.6, c = color, linestyle = 'solid')
        plt.plot(cluster_data['Distance to TX'], cluster_data["RT Matlab"], linewidth=0.6, c = color, linestyle = 'dashed')
        # plt.plot(cluster_data['Distance to TX'], cluster_data["FSPL Matlab"], linewidth=0.6, c = color, linestyle = 'dashdot')
        
        scaler = StandardScaler()
        X = cluster_data['Distance to TX'].values.reshape(-1, 1)
        X_scaled = scaler.fit_transform(X)

        poly = PolynomialFeatures(degree=4)
        X_poly = poly.fit_transform(X_scaled)
        y = cluster_data['RX Power']
        model = LinearRegression()
        model.fit(X_poly, y)
        plt.plot(X, model.predict(X_poly), color=color, label='Real Meas fitted', linestyle = 'solid')

        X_scaled = scaler.fit_transform(X)
        X_poly = poly.fit_transform(X_scaled)
        y = cluster_data["RT Matlab"]
        model = LinearRegression()
        model.fit(X_poly, y)
        plt.plot(X, model.predict(X_poly), color=color, label='RT fitted', linestyle = 'dashed')

        X_scaled = scaler.fit_transform(X)
        X_poly = poly.fit_transform(X_scaled)
        y = cluster_data["FSPL Matlab"]
        model = LinearRegression()
        model.fit(X_poly, y)
        # plt.plot(X, model.predict(X_poly), color=color, label='FSPL fitted', linestyle = 'dashdot')

        plt.title(f"Received Signal Strength in cluster {cluster_id} depending on the distance from the transmitter")
        plt.xlabel("Distance to transmitter")
        plt.ylabel("RX Power")
        plt.grid(True)
        plt.legend()
        plt.show()
#plot_separate_CUSTOM_clusters()


def plot_separate_KMEANS_clusters():  
    for cluster_id, cluster_data in clusters.items():
        plt.figure()  
        color = cluster_colors[cluster_id]  
        plt.scatter(x = cluster_data['Distance to TX'], y = cluster_data['RX Power'], c = color, linewidth=0.4, marker=".", label='Real measurement')
        plt.scatter(x = cluster_data['Distance to TX'], y = cluster_data['RT Matlab'], c = color, linewidth=0.2, marker="^", label='RT model')
        # plt.scatter(x = cluster_data['Distance to TX'], y = cluster_data['FSPL Matlab'], c = color, linewidth=0.2, marker="s", label='FSPL model')
        
        cluster_data.sort_values('Distance to TX', inplace=True)
        plt.plot(cluster_data['Distance to TX'], cluster_data['RX Power'], linewidth=0.6, c = color, linestyle = 'solid')
        plt.plot(cluster_data['Distance to TX'], cluster_data["RT Matlab"], linewidth=0.6, c = color, linestyle = 'dashed')
        # plt.plot(cluster_data['Distance to TX'], cluster_data["FSPL Matlab"], linewidth=0.6, c = color, linestyle = 'dashdot')
        
        scaler = StandardScaler()
        X = cluster_data['Distance to TX'].values.reshape(-1, 1)
        X_scaled = scaler.fit_transform(X)

        poly = PolynomialFeatures(degree=4)
        X_poly = poly.fit_transform(X_scaled)
        y = cluster_data['RX Power']
        model = LinearRegression()
        model.fit(X_poly, y)
        plt.plot(X, model.predict(X_poly), color=color, label='Real Meas fitted', linestyle = 'solid')

        X_scaled = scaler.fit_transform(X)
        X_poly = poly.fit_transform(X_scaled)
        y = cluster_data["RT Matlab"]
        model = LinearRegression()
        model.fit(X_poly, y)
        plt.plot(X, model.predict(X_poly), color=color, label='RT fitted', linestyle = 'dashed')

        X_scaled = scaler.fit_transform(X)
        X_poly = poly.fit_transform(X_scaled)
        y = cluster_data["FSPL Matlab"]
        model = LinearRegression()
        model.fit(X_poly, y)
        # plt.plot(X, model.predict(X_poly), color=color, label='FSPL fitted', linestyle = 'dashdot')

        plt.title(f"Received Signal Strength in cluster {cluster_id} depending on the distance from the transmitter")
        plt.xlabel("Distance to transmitter")
        plt.ylabel("RX Power")
        plt.grid(True)
        plt.legend()
        plt.show()
     
def plot_all_KMEANS_clusters():
    plt.figure(figsize=(10, 8))
    for cluster_id, cluster_data in clusters.items():
        color = cluster_colors[cluster_id]  
        plt.scatter(x = cluster_data['Distance to TX'], y = cluster_data['RX Power'], c = color, linewidth=0.4, marker=".", label=f'Real measurement - Cluster {cluster_id}')
        plt.scatter(x = cluster_data['Distance to TX'], y = cluster_data['RT Matlab'], c = color, linewidth=0.2, marker="^", label=f'RT model - Cluster {cluster_id}')
        # plt.scatter(x = cluster_data['Distance to TX'], y = cluster_data['FSPL Matlab'], c = color, linewidth=0.2, marker="s", label=f'FSPL model - Cluster {cluster_id}')

        cluster_data.sort_values('Distance to TX', inplace=True)
        plt.plot(cluster_data['Distance to TX'], cluster_data['RX Power'], linewidth=0.8, c = color, linestyle = 'solid')
        plt.plot(cluster_data['Distance to TX'], cluster_data["RT Matlab"], linewidth=0.8, c = color, linestyle = 'dashed')
        # plt.plot(cluster_data['Distance to TX'], cluster_data["FSPL Matlab"], linewidth=0.8, c = color, linestyle = 'dashdot')

        poly = PolynomialFeatures(degree=2)
        X = cluster_data['Distance to TX'].values.reshape(-1, 1)
        y = cluster_data['RX Power']
        X_poly = poly.fit_transform(X)
        model = LinearRegression()
        model.fit(X_poly, y)
        plt.plot(X, model.predict(X_poly), color=color, label='Real Meas fitted', linestyle = 'solid')

        poly = PolynomialFeatures(degree=2)
        X = cluster_data['Distance to TX'].values.reshape(-1, 1)
        y = cluster_data["RT Matlab"]
        X_poly = poly.fit_transform(X)
        model = LinearRegression()
        model.fit(X_poly, y)
        plt.plot(X, model.predict(X_poly), color=color, label='RT fitted', linestyle = 'dashed')
        
        poly = PolynomialFeatures(degree=2)
        X = cluster_data['Distance to TX'].values.reshape(-1, 1)
        y = cluster_data["FSPL Matlab"]
        X_poly = poly.fit_transform(X)
        model = LinearRegression()
        model.fit(X_poly, y)
        # plt.plot(X, model.predict(X_poly), color=color, label='FSPL fitted', linestyle = 'dashdot')
    
    plt.title("Received Signal Strength in all clusters depending on the distance from the transmitter")
    plt.xlabel("Distance to transmitter")
    plt.ylabel("RX Power")
    plt.grid(True)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.show()

corr = []

def stat_all():
    distance_to_tx = from_matlab['Distance to TX']
    rx_power = from_matlab['RX Power']
    rt_matlab = from_matlab['RT Matlab']
    delta = rt_matlab - rx_power
    avgdelta = mean(delta)
    rate= rx_power/rt_matlab
    avgrate = mean(rate)
    print(avgrate)
    from_matlab['Corrected RT Matlab'] = from_matlab['RT Matlab']*avgrate  
    
    corrected_rate = mean(rx_power/from_matlab['Corrected RT Matlab'])
    
    plt.figure()  
    color = 'gold'
    from_matlab.sort_values('Distance to TX', inplace=True)

    scaler = StandardScaler()
    X = from_matlab['Distance to TX'].values.reshape(-1, 1)
    X_scaled = scaler.fit_transform(X)

    poly = PolynomialFeatures(degree=4)
    X_poly = poly.fit_transform(X_scaled)
    y = from_matlab['RX Power']
    model1 = LinearRegression()
    model1.fit(X_poly, y)
    plt.plot(X, model1.predict(X_poly), color='blue', label='Valós mérés', linestyle = 'solid')

    X_scaled = scaler.fit_transform(X)
    X_poly = poly.fit_transform(X_scaled)
    y = from_matlab['Corrected RT Matlab']
    model2 = LinearRegression()
    model2.fit(X_poly, y)
    plt.plot(X, model2.predict(X_poly), color='green', label='Korrigált RT szimuláció', linestyle = 'solid')
    
    X_scaled = scaler.fit_transform(X)
    X_poly = poly.fit_transform(X_scaled)
    y = from_matlab['RT Matlab']
    model3 = LinearRegression()
    model3.fit(X_poly, y)
    plt.plot(X, model3.predict(X_poly), color='red', label='RT szimuláció', linestyle = 'solid')


    plt.title(f"A fogadott jel erőssége a teljes mérés során \na küldőtől való távolság függvényében")
    plt.xlabel("Távolség a küldőtől [m]")
    plt.ylabel("Fogadott jel erőssége [dBm]")
    plt.grid(True)
    plt.legend()
    plt.show()

    correlation = np.corrcoef(from_matlab['RX Power'], from_matlab['RT Matlab'])[0, 1]
    correlation_corrected = np.corrcoef(from_matlab['RX Power'], from_matlab['Corrected RT Matlab'])[0, 1]
    print(f'The correlation is {correlation:.3f} \n The correlation of the corrected data is {correlation_corrected:.3f}') 
    #corr.append(f"The correlation in cluster {cluster_id} is {correlation:.2f}")
    #corr.append(from_matlab, correlation, correlation_corrected))
     
    print(f'\n The average difference was: {avgrate:.3f}, and now it is {corrected_rate:.3f}')
    
stat_all()


def stat():
    for cluster_id, cluster_data in clusters.items():
        distance_to_tx = cluster_data['Distance to TX']
        rx_power = cluster_data['RX Power']
        rt_matlab = cluster_data['RT Matlab']
        delta = rt_matlab - rx_power
        avgdelta = mean(delta)
        rate= rx_power/rt_matlab
        avgrate = mean(rate)
        #avgrate = 1.065
        print(avgrate)        
        Corrected_rt = rt_matlab * avgrate
        # Corrected_rt = Corrected_rt[np.abs(stats.zscore(Corrected_rt)) < 3]
        df = pd.DataFrame({"RX Power": rx_power, "RT Matlab": rt_matlab, "Distance to TX": distance_to_tx})
        Corrected_df = df[np.abs(stats.zscore(df["RX Power"])) < 2]
        Corrected_df.loc[:, 'RT Matlab'] = Corrected_df['RT Matlab']*avgrate
        Corrected_df = Corrected_df[np.abs(stats.zscore(Corrected_df["RT Matlab"])) < 2]

        plt.figure()  
        color = cluster_colors[cluster_id]  
        # plt.scatter(x = Corrected_df['Distance to TX'], y = Corrected_df['RX Power'], c = color, linewidth=0.4, marker=".", label='Real measurement')
        # plt.scatter(x = Corrected_df['Distance to TX'], y = Corrected_df['RT Matlab'], c = color, linewidth=0.2, marker="^", label='RT model')
        # plt.scatter(x = cluster_data['Distance to TX'], y = cluster_data['FSPL Matlab'], c = color, linewidth=0.2, marker="s", label='FSPL model')
        
        cluster_data.sort_values('Distance to TX', inplace=True)
        # plt.plot(Corrected_df['Distance to TX'], Corrected_df['RX Power'], linewidth=0.6, c = color, linestyle = 'solid')
        # plt.plot(Corrected_df['Distance to TX'], Corrected_df['RT Matlab'], linewidth=0.6, c = color, linestyle = 'dashed')
        # plt.plot(cluster_data['Distance to TX'], cluster_data["FSPL Matlab"], linewidth=0.6, c = color, linestyle = 'dashdot')
        
        scaler = StandardScaler()
        X = Corrected_df['Distance to TX'].values.reshape(-1, 1)
        X_scaled = scaler.fit_transform(X)

        poly = PolynomialFeatures(degree=4)
        X_poly = poly.fit_transform(X_scaled)
        y = Corrected_df['RX Power']
        model1 = LinearRegression()
        model1.fit(X_poly, y)
        plt.plot(X, model1.predict(X_poly), color=color, label='Real Meas fitted', linestyle = 'solid')

        X_scaled = scaler.fit_transform(X)
        X_poly = poly.fit_transform(X_scaled)
        y = Corrected_df['RT Matlab']
        model2 = LinearRegression()
        model2.fit(X_poly, y)
        plt.plot(X, model2.predict(X_poly), color=color, label='RT fitted', linestyle = 'dashed')


        plt.title(f"Received Signal Strength in cluster {cluster_id} depending on the distance from the transmitter")
        plt.xlabel("Distance to transmitter")
        plt.ylabel("RX Power")
        plt.grid(True)
        plt.legend()
        plt.show()

        correlation = np.corrcoef(Corrected_df['RX Power'], Corrected_df['RT Matlab'])[0, 1]
        #corr.append(f"The correlation in cluster {cluster_id} is {correlation:.2f}")
        corr.append((cluster_id, correlation))

        divdiff = pd.DataFrame({"Difference":[delta], "Rate":[rate]})
        #print(divdiff, avgdelta, avgrate)
        
        def f(x):
            x_scaled = scaler.transform(np.array([[x]]))
            x_poly = poly.transform(x_scaled)
            return model1.predict(x_poly)  # model1 is the model for 'RX Power'

        def g(x):
            x_scaled = scaler.transform(np.array([[x]]))
            x_poly = poly.transform(x_scaled)
            return model2.predict(x_poly)  # model2 is the model for 'RT Matlab'

        # Define the function to integrate
        def h(x):
            return np.abs(f(x) - g(x))

        # Integrate |f(x) - g(x)| from a to b
        a = Corrected_df['Distance to TX'].min()  # lower limit
        b = Corrected_df['Distance to TX'].max()  # upper limit
        result, error = quad(h, a, b)

        print(f"The distance between the two functions is approximately {result} with an error of {error}")
        
    for cluster_id, correlation in corr:
        print(f"The correlation in cluster {cluster_id} is {correlation:.2f}")
        
    print(f'\n The average difference is: {avgrate}')



# #def m_rt_correlation():
# #    for cluster_id, cluster_data in clusters.items():
#         rx_power = cluster_data['RX Power']
#         rt_matlab = cluster_data['RT Matlab']

#         correlation = np.corrcoef(rx_power, rt_matlab)[0, 1]
#         print(f"The correlation between 'RX Power' and 'RT Matlab' in cluster {cluster_id} is {correlation:.2f}")

#print(kmeans)

#create_df_to_matlab()
#plot_customClusters(map)
#plot_to_osm()
#plot_all_clusters()
#plot_separate_clusters()

#m_rt_correlation()

#plt.close('all')