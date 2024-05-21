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

%% PILOT
numSubCar = 1024;
pilotGap = 20;
pilotsPerSym = 52;

s = RandStream("dsfmt19937","Seed",15);
pilot = (randi(s,[0 1],pilotsPerSym,1)-0.5)*2;

%pilotInd = (1:pilotGap:numSubCar).';
pilotInd = [25
50
75
100
125
150
175
200
225
250
275
300
325
350
375
400
425
450
475
500
525
550
575
600
625
650
675
700
725
750
775
800
825
850
875
900
925
950
975
1000];

dcIdx = (numSubCar/2)+1;
if any(pilotInd == dcIdx)
    pilotInd(floor(length(pilotInd)/2)+1:end) = 1 + ...
        pilotInd(floor(length(pilotInd)/2)+1:end);
end

%% NOISE

data = load("Stoczek_V2.mat");
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
        "Latitude",stillLAT, ...
        "Longitude",stillLON, ...
        "AntennaHeight",1.5);
%show(rx)

tx = txsite.empty(data_length(1), 0);
ss = zeros(data_length(1), 1);
d = zeros(data_length(1), 1);
fspla = zeros(data_length(1), 1);
delta = zeros(data_length(1), 1);
sinr = zeros(data_length(1), 1);

disp(size(tx));
disp(size(ss));


for i = 1:size(waypointsLON)
    tx(i) = txsite("Name","Transmitter", ...
    "Latitude",waypointsLAT(i), ...
    "Longitude",waypointsLON(i), ...
    "AntennaHeight",1.5, ...
    "TransmitterPower",0.1, ...
    "TransmitterFrequency",5.9e9);

    %raytrace(tx,rx(i),rtpm)

    ss(i) = (sigstrength(rx,tx(i),rtpm)); % , *1.18
    correction = ((1.1372268044762563-1)/2)+1;
    if Mode == 1
        ss(i)  = ss(i)*correction;
        %ss(i)  = ss(i)*1.1372268044762563;
        if (ss(i) == -Inf) %or (ss(i) <= -85)
            ss(i) = -120;
        end
    elseif Mode == 2
        ss(i) = ss(i)*1.1052733659745277;
        if (ss(i) == -Inf) %or (ss(i) <= -95)
           ss(i) = -120;
        end
    end

    d(i) = distance(tx(i),rx);
    fspla(i) = Pt - fspl(d(i),lambda);

end

RxPower = [waypoints, ss'];


