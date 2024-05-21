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

data = load("v2.mat");
geographicReference = [data.data.GeographicReference];

%% EGO car data
egoWP = data.data.ActorSpecifications(1,1).Waypoints(:,[1,2]);
[egoLAT,egoLON] = local2latlon(egoWP(:,1), egoWP(:,2), 0, geographicReference);


%% Other cars data

v1 = data.data.ActorSpecifications(1,2).Waypoints(:,[1,2]);
[v1LAT, v1LON] = local2latlon(v1(:,1), v1(:,2), 0, geographicReference);

v2 = data.data.ActorSpecifications(1,3).Waypoints(:,[1,2]);
[v2LAT, v2LON] = local2latlon(v2(:,1), v2(:,2), 0, geographicReference);

v3 = data.data.ActorSpecifications(1,4).Waypoints(:,[1,2]);
[v3LAT, v3LON] = local2latlon(v3(:,1), v3(:,2), 0, geographicReference);

v4 = data.data.ActorSpecifications(1,5).Waypoints(:,[1,2]);
[v4LAT, v4LON] = local2latlon(v4(:,1), v4(:,2), 0, geographicReference);

v5 = data.data.ActorSpecifications(1,6).Waypoints(:,[1,2]);
[v5LAT, v5LON] = local2latlon(v5(:,1), v5(:,2), 0, geographicReference);

v6 = data.data.ActorSpecifications(1,7).Waypoints(:,[1,2]);
[v6LAT, v6LON] = local2latlon(v6(:,1), v6(:,2), 0, geographicReference);


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

% rx = rxsite("Name","Receiver", ...
%         "Latitude",egoLAT, ...
%         "Longitude",egoLON, ...
%         "AntennaHeight",1.5);
%show(rx)

sizeEgoWP = length(egoWP);

%% V1
sizeV1WP = length(v1);

RxPowerV1 = zeros(sizeEgoWP+2, sizeV1WP+2);

for i = 3:sizeV1WP+2
    RxPowerV1(1,i) = v1(i-2,1);
    RxPowerV1(2,i) = v1(i-2,2);
end

for i = 3:sizeEgoWP+2
    RxPowerV1(i,1) = egoWP(i-2,1);
    RxPowerV1(i,2) = egoWP(i-2,2);
end

for i = 1:(size(egoLAT,1))
    rx(i) = rxsite("Name","Receiver", ...
            "Latitude",egoLAT(i), ...
            "Longitude",egoLON(i), ...
            "AntennaHeight",1.5);
    for j = 1:(size(v1LAT,1))
        tx(j) = txsite("Name","Transmitter", ...
            "Latitude",v1LAT(j), ...
            "Longitude",v1LON(j), ...
            "AntennaHeight",1.5, ...
            "TransmitterPower",0.1, ...
            "TransmitterFrequency",5.9e9);

        RxPowerV1(i+2,j+2) = sigstrength(rx(i),tx(j),rtpm);

        correction = ((1.1372268044762563-1)/2)+1;
        if Mode == 1
            RxPowerV1(i+2,j+2)  = RxPowerV1(i+2,j+2)*correction;
            %ss(i)  = ss(i)*1.1372268044762563;
            if (RxPowerV1(i+2,j+2) == -Inf) %or (ss(i) <= -85)
               RxPowerV1(i+2,j+2) = -120;
            end

        elseif Mode == 2
            RxPowerV1(i+2,j+2) = RxPowerV1(i+2,j+2)*1.1052733659745277;
            if (RxPowerV1(i+2,j+2) == -Inf) %or (ss(i) <= -95)
                RxPowerV1(i+2,j+2) = -120;
            end
        end
    end
end


%% V2
sizeV2WP = length(v2);

RxPowerV2 = zeros(sizeEgoWP+2, sizeV2WP+2);

for i = 3:sizeV2WP+2
    RxPowerV2(1,i) = v2(i-2,1);
    RxPowerV2(2,i) = v2(i-2,2);
end

for i = 3:sizeEgoWP+2
    RxPowerV2(i,1) = egoWP(i-2,1);
    RxPowerV2(i,2) = egoWP(i-2,2);
end

for i = 1:(size(egoLAT,1))
    rx(i) = rxsite("Name","Receiver", ...
            "Latitude",egoLAT(i), ...
            "Longitude",egoLON(i), ...
            "AntennaHeight",1.5);
    for j = 1:(size(v2LAT,1))
        tx(j) = txsite("Name","Transmitter", ...
            "Latitude",v2LAT(j), ...
            "Longitude",v2LON(j), ...
            "AntennaHeight",1.5, ...
            "TransmitterPower",0.1, ...
            "TransmitterFrequency",5.9e9);

        RxPowerV2(i+2,j+2) = sigstrength(rx(i),tx(j),rtpm);

        correction = ((1.1372268044762563-1)/2)+1;
        if Mode == 1
            RxPowerV2(i+2,j+2)  = RxPowerV2(i+2,j+2)*correction;
            %ss(i)  = ss(i)*1.1372268044762563;
            if (RxPowerV2(i+2,j+2) == -Inf) %or (ss(i) <= -85)
               RxPowerV2(i+2,j+2) = -120;
            end

        elseif Mode == 2
            RxPowerV2(i+2,j+2) = RxPowerV2(i+2,j+2)*1.1052733659745277;
            if (RxPowerV2(i+2,j+2) == -Inf) %or (ss(i) <= -95)
                RxPowerV2(i+2,j+2) = -120;
            end
        end
    end
end
%% V3
sizeV3WP = length(v3);

RxPowerV3 = zeros(sizeEgoWP+2, sizeV3WP+2);

for i = 3:sizeV3WP+2
    RxPowerV3(1,i) = v3(i-2,1);
    RxPowerV3(2,i) = v3(i-2,2);
end

for i = 3:sizeEgoWP+2
    RxPowerV3(i,1) = egoWP(i-2,1);
    RxPowerV3(i,2) = egoWP(i-2,2);
end

for i = 1:(size(egoLAT,1))
    rx(i) = rxsite("Name","Receiver", ...
            "Latitude",egoLAT(i), ...
            "Longitude",egoLON(i), ...
            "AntennaHeight",1.5);
    for j = 1:(size(v3LAT,1))
        tx(j) = txsite("Name","Transmitter", ...
            "Latitude",v3LAT(j), ...
            "Longitude",v3LON(j), ...
            "AntennaHeight",1.5, ...
            "TransmitterPower",0.1, ...
            "TransmitterFrequency",5.9e9);

        RxPowerV3(i+2,j+2) = sigstrength(rx(i),tx(j),rtpm);

        correction = ((1.1372268044762563-1)/2)+1;
        if Mode == 1
            RxPowerV3(i+2,j+2)  = RxPowerV3(i+2,j+2)*correction;
            %ss(i)  = ss(i)*1.1372268044762563;
            if (RxPowerV3(i+2,j+2) == -Inf) %or (ss(i) <= -85)
               RxPowerV3(i+2,j+2) = -120;
            end

        elseif Mode == 2
            RxPowerV3(i+2,j+2) = RxPowerV3(i+2,j+2)*1.1052733659745277;
            if (RxPowerV3(i+2,j+2) == -Inf) %or (ss(i) <= -95)
                RxPowerV3(i+2,j+2) = -120;
            end
        end
    end
end

%% V4
sizeV4WP = length(v4);

RxPowerV4 = zeros(sizeEgoWP+2, sizeV4WP+2);

for i = 3:sizeV4WP+2
    RxPowerV4(1,i) = v4(i-2,1);
    RxPowerV4(2,i) = v4(i-2,2);
end

for i = 3:sizeEgoWP+2
    RxPowerV4(i,1) = egoWP(i-2,1);
    RxPowerV4(i,2) = egoWP(i-2,2);
end

for i = 1:(size(egoLAT,1))
    rx(i) = rxsite("Name","Receiver", ...
            "Latitude",egoLAT(i), ...
            "Longitude",egoLON(i), ...
            "AntennaHeight",1.5);
    for j = 1:(size(v4LAT,1))
        tx(j) = txsite("Name","Transmitter", ...
            "Latitude",v4LAT(j), ...
            "Longitude",v4LON(j), ...
            "AntennaHeight",1.5, ...
            "TransmitterPower",0.1, ...
            "TransmitterFrequency",5.9e9);

        RxPowerV4(i+2,j+2) = sigstrength(rx(i),tx(j),rtpm);

        correction = ((1.1372268044762563-1)/2)+1;
        if Mode == 1
            RxPowerV4(i+2,j+2)  = RxPowerV4(i+2,j+2)*correction;
            %ss(i)  = ss(i)*1.1372268044762563;
            if (RxPowerV4(i+2,j+2) == -Inf) %or (ss(i) <= -85)
               RxPowerV4(i+2,j+2) = -120;
            end

        elseif Mode == 2
            RxPowerV4(i+2,j+2) = RxPowerV4(i+2,j+2)*1.1052733659745277;
            if (RxPowerV4(i+2,j+2) == -Inf) %or (ss(i) <= -95)
                RxPowerV4(i+2,j+2) = -120;
            end
        end
    end
end

%% V5
sizeV5WP = length(v5);

RxPowerV5 = zeros(sizeEgoWP+2, sizeV5WP+2);

for i = 3:sizeV5WP+2
    RxPowerV5(1,i) = v5(i-2,1);
    RxPowerV5(2,i) = v5(i-2,2);
end

for i = 3:sizeEgoWP+2
    RxPowerV5(i,1) = egoWP(i-2,1);
    RxPowerV5(i,2) = egoWP(i-2,2);
end

for i = 1:(size(egoLAT,1))
    rx(i) = rxsite("Name","Receiver", ...
            "Latitude",egoLAT(i), ...
            "Longitude",egoLON(i), ...
            "AntennaHeight",1.5);
    for j = 1:(size(v5LAT,1))
        tx(j) = txsite("Name","Transmitter", ...
            "Latitude",v5LAT(j), ...
            "Longitude",v5LON(j), ...
            "AntennaHeight",1.5, ...
            "TransmitterPower",0.1, ...
            "TransmitterFrequency",5.9e9);

        RxPowerV5(i+2,j+2) = sigstrength(rx(i),tx(j),rtpm);

        correction = ((1.1372268044762563-1)/2)+1;
        if Mode == 1
            RxPowerV5(i+2,j+2)  = RxPowerV5(i+2,j+2)*correction;
            %ss(i)  = ss(i)*1.1372268044762563;
            if (RxPowerV5(i+2,j+2) == -Inf) %or (ss(i) <= -85)
               RxPowerV5(i+2,j+2) = -120;
            end

        elseif Mode == 2
            RxPowerV5(i+2,j+2) = RxPowerV5(i+2,j+2)*1.1052733659745277;
            if (RxPowerV5(i+2,j+2) == -Inf) %or (ss(i) <= -95)
                RxPowerV5(i+2,j+2) = -120;
            end
        end
    end
end
%% V6
sizeV6WP = length(v6);

RxPowerV6 = zeros(sizeEgoWP+2, sizeV6WP+2);

for i = 3:sizeV6WP+2
    RxPowerV6(1,i) = v6(i-2,1);
    RxPowerV6(2,i) = v6(i-2,2);
end

for i = 3:sizeEgoWP+2
    RxPowerV6(i,1) = egoWP(i-2,1);
    RxPowerV6(i,2) = egoWP(i-2,2);
end

for i = 1:(size(egoLAT,1))
    rx(i) = rxsite("Name","Receiver", ...
            "Latitude",egoLAT(i), ...
            "Longitude",egoLON(i), ...
            "AntennaHeight",1.5);
    for j = 1:(size(v6LAT,1))
        tx(j) = txsite("Name","Transmitter", ...
            "Latitude",v6LAT(j), ...
            "Longitude",v6LON(j), ...
            "AntennaHeight",1.5, ...
            "TransmitterPower",0.1, ...
            "TransmitterFrequency",5.9e9);

        RxPowerV6(i+2,j+2) = sigstrength(rx(i),tx(j),rtpm);

        correction = ((1.1372268044762563-1)/2)+1;
        if Mode == 1
            RxPowerV6(i+2,j+2)  = RxPowerV6(i+2,j+2)*correction;
            %ss(i)  = ss(i)*1.1372268044762563;
            if (RxPowerV6(i+2,j+2) == -Inf) %or (ss(i) <= -85)
               RxPowerV6(i+2,j+2) = -120;
            end

        elseif Mode == 2
            RxPowerV6(i+2,j+2) = RxPowerV6(i+2,j+2)*1.1052733659745277;
            if (RxPowerV6(i+2,j+2) == -Inf) %or (ss(i) <= -95)
                RxPowerV6(i+2,j+2) = -120;
            end
        end
    end
end


%% Ego Vehicle parameters
nrWheelsFr = 2; % Number of wheels on front axle
nrWheelsRe = 2; % Number of wheels on rear axle
mEgo = 1500; % Vehicle mass, m [kg]
a = 1.4; % Longitudinal distance from center of mass to front axle, a [m]
b = 1.6; % Longitudinal distance from center of mass to rear axle, b [m]
h = 0.35; % Vertical distance from center of mass to axle plane, h [m]

Cy_f = 12e3; % Front tire corner stiffness, Cy_f [N/rad]
Cy_r = 11e3; % Rear tire axle corner stiffness, Cy_r [N/rad]
sigma_f = 0.1; % Front tire(s) relaxation length, sigma_f [m]
sigma_r = 0.1; % Rear tire(s) relaxation length, sigma_r [m]
Izz = 4000; % Yaw polar inertia, Izz [kg*m^2] 

%% ACTOR IDs
LeadID = 2;
InterferingID = 3;
ThresholdID = 1;

%% Adaptív tempomat modell
tau = 0.5;
m = 2000;
Fz_f = 1300/m;
Fz_r = 700/m;

%% Environment
Grade = 0;
WindXYZ = [0 0 0];

%% Járművek kezdeti értékei:
a_lead = 2;
v0_lead = 20;   
x0_lead = 50;

v0_con = 30;
x0_con = 10;

t_gap = 1.4;

v_set = 30;

%% EGO WAYPOINTS MATRIX
zeroforwp = zeros(size(egoWP,1),1);
waypoints = [egoWP(:,2) egoWP(:,1), zeroforwp];



% [5 -1.6 0;
%     60 -1.6 0;
%     150 -1.6 0;
%     300 -1.6 0;
%     395 -1.6 0];




% Adaptive Cruise control block parameters

G_con = tf(1,[0.5,1,0]);        %  Linear model from longitudinal acceleration to longitudinal velocity
vinit = 20;                     %  Initial condition for longitudinal velocity (m/s)
D_default = 10;                 %  Default spacing (m)
vmax = 35;                      %  Maximum velocity (m/s)
amin = -3;                      %  Minimum longitudinal acceleration (m/s^2)
amax = 2;                       %  Maximum longitudinal acceleration (m/s^2)
Prediction_horizon = 30;        %  Prediction horizon (steps)
Controller_behaivour = 0.5;     %  Controller behavour [More robust 0<----->1 More aggressive]
vmin = 0;

%  Multi-Object Tracker
assigThresh = 30;         % Threshold for assigning detections to tracks
numTracks = 200;          % Maximum number of tracks
numSensors = 20;          % Maximum number of sensors

positionSensor = 1;


%% Lanes bus signal
% Left
left(1) = Simulink.BusElement;
left(1).Name = "Curvature";
left(2) = Simulink.BusElement;
left(2).Name = "CurvatureDerivative";
left(3) = Simulink.BusElement;
left(3).Name = "HeadingAngle";
left(4) = Simulink.BusElement;
left(4).Name = "LateralOffset";
left(5) = Simulink.BusElement;
left(5).Name = "Strength";
Left = Simulink.Bus;
Left.Elements = left;

% Right
right(1) = Simulink.BusElement;
right(1).Name = "Curvature";
right(2) = Simulink.BusElement;
right(2).Name = "CurvatureDerivative";
right(3) = Simulink.BusElement;
right(3).Name = "HeadingAngle";
right(4) = Simulink.BusElement;
right(4).Name = "LateralOffset";
right(5) = Simulink.BusElement;
right(5).Name = "Strength";
Right = Simulink.Bus;
Right.Elements = right;

% Lanes
lanes(1) = Simulink.BusElement;
lanes(1).Name = "Left";
lanes(2) = Simulink.BusElement();
lanes(2).Name = "Right";
Lanes = Simulink.Bus;
Lanes.Elements = lanes;

InternalBuses = Simulink.Bus;
InternalBuses.Elements = left(1:4);