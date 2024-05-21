clc
clear 

%% Variant
% 3/4 64 QAM: M = 1
% 1/2 QPSK: M = 2
Mode = 1; 

output_size = 0;
if Mode == 1
    vector_size = 288;
    puncture_vector = [1;1;0;1;1;0];
elseif Mode == 2
    vector_size = 480;
    puncture_vector = [1; 1];
end

%%

sampleTime = 0.1;
M = 2;
Nbps = 16;
EbN0aa = 35;
phaseNoise = -76;
freqOffset = 1000;

% pilot1 = 1;
% pilot2 = exp(1i*pi/2);
% pilot3 = exp(1i*pi);
% pilot4 = exp(1i*3*pi/2);

vehicles = 3;


freq = 5.9e9;
c = physconst('LightSpeed');
lambda = freq/c;



%% Positions, distances bus
%Positions, Distances
PosDist(1) = Simulink.BusElement;
PosDist(1).Name = "Position";
PosDist(2) = Simulink.BusElement();
PosDist(2).Name = "Distances";
PositionsDistances = Simulink.Bus;
PositionsDistances.Elements = PosDist;

%% Actors bus

actors(1) = Simulink.BusElement;
actors(1).Name = "ActorID";
actors(2) = Simulink.BusElement();
actors(2).Name = "Position";
actors(2).Dimensions = [1,3];
actors(3) = Simulink.BusElement;
actors(3).Name = "Velocity";
actors(3).Dimensions = [1,3];
actors(4) = Simulink.BusElement;
actors(4).Name = "Roll";
actors(5) = Simulink.BusElement;
actors(5).Name = "Pitch";
actors(6) = Simulink.BusElement;
actors(6).Name = "Yaw";
actors(7) = Simulink.BusElement;
actors(7).Name = "AngularVelocity";
actors(7).Dimensions = [1,3];

Actors = Simulink.Bus;
Actors.Elements = actors;


%% NOISE

data = load("Bartok.mat");
geographicReference = [data.data.GeographicReference];

%% EGO car data
egoWP = data.data.ActorSpecifications(1,1).Waypoints(:,[1,2]);
[egoLAT,egoLON] = local2latlon(egoWP(:,1), egoWP(:,2), 0, geographicReference);

%% Other cars data
numCars = 7; % total number of cars including the EGO car
carLAT = cell(numCars, 1);
carLON = cell(numCars, 1);

for i = 2:numCars
    v = data.data.ActorSpecifications(1,i).Waypoints(:,[1,2]);
    [carLAT{i}, carLON{i}] = local2latlon(v(:,1), v(:,2), 0, geographicReference);
end


%% FSPL
fc = 5.9e9; % Hz
lambda = physconst('LightSpeed')/fc;
Pt = 20; %dBm

%% Raytrace
%viewer = siteviewer("Buildings","J_St_osm_map.osm","Basemap","topographic","Terrain","gmted2010");


rtpm = propagationModel("raytracing", ...
    "Method","sbr", ...
    "MaxAbsolutePathLoss", 120,...
    "MaxNumReflections",8, ...
    "BuildingsMaterial","glass", ...
    "TerrainMaterial","concrete");

    % "BuildingsMaterialPermittivity",1.5,...
    % "BuildingsMaterialConductivity",0.0064437,...
    % "TerrainMaterialPermittivity",1.5,...
    % "TerrainMaterialConductivity",0.0064437

% cipm = propagationModel("close-in");

% coverage(tx(i),rtpm, ...
%     "SignalStrengths", -120:-20, ...
%     "MaxRange",250, ...
%     "Resolution",3, ...
%     "Transparency",0.6);

data_length = size(data);

rx = rxsite("Name","Receiver", ...
        "Latitude",egoLAT, ...
        "Longitude",egoLON, ...
        "AntennaHeight",1.5);
%show(rx)

tx = {txsite.empty(data_length(1), 0)};
ss = {zeros(data_length(1), 1)};
d = zeros(data_length(1), 1);
fspla = zeros(data_length(1), 1);
delta = zeros(data_length(1), 1);
sinr = zeros(data_length(1), 1);

ss = cell(size(carLAT));

for i = 1:size(carLAT, 1)
    for j = 1:size(carLAT{i}, 1)
        tx{i}(j) = txsite("Name","Transmitter", ...
            "Latitude",carLAT{i}(j), ...
            "Longitude",carLON{i}(j), ...
            "AntennaHeight",1.5, ...
            "TransmitterPower",0.1, ...
            "TransmitterFrequency",5.9e9);
        
        ss{i} = (sigstrength(rx,tx{i}(j),rtpm));

        %raytrace(tx,rx(i),rtpm
        correction = ((1.1372268044762563-1)/2)+1;
        if Mode == 1
            if (ss{i}(j) == -Inf)
                ss{i}(j) = -120;
            end
            ss{i}  = ss{i}*correction;
            %ss(i)  = ss(i)*1.1372268044762563;            
        elseif Mode == 2
            if (ss{i}(j) == -Inf)
               ss{i}(j) = -120;
            end
            ss{i} = ss{i}*1.1052733659745277;
        end
        
    end
        
    % d(i) = distance(tx(i),rx);
    % fspla(i) = Pt - fspl(d(i),lambda);

end

RxPower = [waypoints, ss'];

% %% EGO car data
% egoWP = data.data.ActorSpecifications(1,1).Waypoints(:,[1,2]);
% [egoLAT,egoLON] = local2latlon(egoWP(:,1), egoWP(:,2), 0, geographicReference);
% 
% 
% %% Other cars data
% 
% v1 = data.data.ActorSpecifications(1,2).Waypoints(:,[1,2]);
% [v1LAT, v1LON] = local2latlon(v1(:,1), v1(:,2), 0, geographicReference);
% 
% v2 = data.data.ActorSpecifications(1,3).Waypoints(:,[1,2]);
% [v2LAT, v2LON] = local2latlon(v2(:,1), v2(:,2), 0, geographicReference);
% 
% v3 = data.data.ActorSpecifications(1,4).Waypoints(:,[1,2]);
% [v3LAT, v3LON] = local2latlon(v3(:,1), v3(:,2), 0, geographicReference);
% 
% v4 = data.data.ActorSpecifications(1,5).Waypoints(:,[1,2]);
% [v4LAT, v4LON] = local2latlon(v4(:,1), v4(:,2), 0, geographicReference);
% 
% v5 = data.data.ActorSpecifications(1,6).Waypoints(:,[1,2]);
% [v5LAT, v5LON] = local2latlon(v5(:,1), v5(:,2), 0, geographicReference);
% 
% v6 = data.data.ActorSpecifications(1,7).Waypoints(:,[1,2]);
% [v6LAT, v6LON] = local2latlon(v6(:,1), v6(:,2), 0, geographicReference);
