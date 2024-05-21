clc
clear
%% Import and handle data

csv = readtable('Python\Main\Data1\MIEV\adr\logs\lap2_33dBm.csv');
data = table2array(csv(5:5:end, [4,5,2]));

%% FSPL
fc = 5.9e9; % Hz
lambda = physconst('LightSpeed')/fc;
Pt = 33; %dBm

%% Raytrace
viewer = siteviewer("Buildings","Stoczek.osm","Basemap","topographic","Terrain","gmted2010");

tx = txsite("Name","Transmitter", ...
    "Latitude",47.4791844, ...
    "Longitude",19.0561957, ...
    "AntennaHeight",1.5, ...
    "TransmitterPower",0.1, ...
    "TransmitterFrequency",5.9e9);
show(tx)

rtpm = propagationModel("raytracing", ...
    "Method","sbr", ...
    "MaxNumReflections",3, ...
    "BuildingsMaterial","concrete", ...
    "TerrainMaterial","concrete");

cipm = propagationModel("close-in");

coverage(tx,rtpm, ...
    "SignalStrengths", -120:-5, ...
    "MaxRange",200, ...
    "Resolution",3, ...
    "Transparency",0.6);

data_length = size(data);

rx = rxsite.empty(data_length(1), 0);
ss = zeros(data_length(1), 1);
d = zeros(data_length(1), 1);
fspla = zeros(data_length(1), 1);

for i = 6
    rx(i) = rxsite("Name","Receiver", ...
            "Latitude",data(i,1), ...
            "Longitude",data(i,2), ...
            "AntennaHeight",1.5);
    %raytrace(tx,rx(i),rtpm)

    ss(i) = sigstrength(rx(i),tx,rtpm);

    d(i) = distance(tx,rx(i));
    fspla(i) = Pt - fspl(d(i),lambda);

end

data = table([data, ss, fspla]);
csv_filename = 'rx_data.csv'; % Specify your desired filename
writetable(data, csv_filename);


%rt = raytrace(tx,rx(i),rtpm);
% ss1 = sigstrength(rx1,tx,rtpm);
% ss2 = sigstrength(rx2,tx,rtpm);     
% ss3 = sigstrength(rx3,tx,rtpm);
% ss4 = sigstrength(rx3,tx,rtpm);

%% Pathloss Model

% rt = raytrace(tx,rx4,rtpm);

%% Display
% disp("Signal strength at receivers: " + ss1 + ", " + ss2 + ", " + ss3 + ", " + ss4)
% %disp("Signal strenght with PL model: " + pl + ", " + pl2 + ", " + pl3 + ", " + pl4)
% disp("Signal strength with FSPL at receivers: " + fspl1 + ", " + fspl2 + ", " + fspl3 + ", " + fspl4)
