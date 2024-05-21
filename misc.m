clc
clear

%% Extracting data from Driving Scenario

data = load("Stoczek.mat");
geographicReference = [data.data.GeographicReference];

%% Moving car data
waypoints = data.data.ActorSpecifications(1,1).Waypoints(:,[1,2]);
[waypointsLAT,waypointsLON] = local2latlon(waypoints(:,1), waypoints(:,2), 0, geographicReference);

% disp('Converted Waypoints (Latitude, Longitude):');
% disp(waypointsLATLON);

%% Still car data

still = data.data.ActorSpecifications(1,2).Position;
[stillLAT, stillLON] = local2latlon(still(:,1), still(:,2), 0, geographicReference);


%% FSPL
fc = 5.9e9; % Hz
lambda = physconst('LightSpeed')/fc;
Pt = 33; %dBm

%% Raytrace
viewer = siteviewer("Buildings","J_St_osm_map.osm","Basemap","topographic","Terrain","gmted2010");

tx = txsite("Name","Transmitter", ...
    "Latitude",stillLAT, ...
    "Longitude",stillLON, ...
    "AntennaHeight",1.5, ...
    "TransmitterPower",1.995262315, ...
    "TransmitterFrequency",5.9e9);
show(tx)

rtpm = propagationModel("raytracing", ...
    "Method","sbr", ...
    "MaxAbsolutePathLoss", 120,...
    "MaxNumReflections",5, ...
    "BuildingsMaterial","wood", ...
    "TerrainMaterial","vegetation");

    % "BuildingsMaterialPermittivity",1.5,...
    % "BuildingsMaterialConductivity",0.0064437,...
    % "TerrainMaterialPermittivity",1.5,...
    % "TerrainMaterialConductivity",0.0064437

% cipm = propagationModel("close-in");

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
delta = zeros(data_length(1), 1);
sinr = zeros(data_length(1), 1);

for i = 1:size(waypointsLON)
    rx(i) = rxsite("Name","Receiver", ...
            "Latitude",waypointsLAT(i), ...
            "Longitude",waypointsLON(i), ...
            "AntennaHeight",1.5);
    raytrace(tx,rx(i),rtpm)

    ss(i) = (sigstrength(rx(i),tx,rtpm))*1.325;
    if ss(i) == -Inf
        ss(i) = -120;
    end

    % delta(i) = -(data(i,4)-ss(i));

    %sinr(i) = sinr

    d(i) = distance(tx,rx(i));
    fspla(i) = Pt - fspl(d(i),lambda);

end

