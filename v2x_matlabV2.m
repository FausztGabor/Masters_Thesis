clc
clear 

sampleTime = 0.1;
M = 2;
Nbps = 16;
EbN0aa = 35;
phaseNoise = -76;
freqOffset = 1000;

pilot1 = 1;
pilot2 = exp(1i*pi/2);
pilot3 = exp(1i*pi);
pilot4 = exp(1i*3*pi/2);

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

%% PropagationModel

% pm(1) = Simulink.BusElement;
% pm(1).Name = "raytracing";
pm(1) = Simulink.BusElement;
pm(1).Name = char("Method");
pm(1).DataType = "char";
pm(2) = Simulink.BusElement;
pm(2).Name = char("maxNumReflections");
pm(3) = Simulink.BusElement;
pm(3).Name = char("BuildingsMaterial");
pm(3).DataType = "char";
pm(4) = Simulink.BusElement;
pm(4).Name = char("TerrainMaterial");
pm(4).DataType = "char";

propMod = Simulink.Bus;
propMod.Elements = pm;



%% ZEROACTORS

ZeroActors = struct(...
    'ActorID',0,...
    'Position', [1000 1000 1000], ...
    'Velocity', [0 0 0], ...
    'Roll', 0, ...
    'Pitch', 0, ...
    'Yaw', 0, ...
    'AngularVelocity', [0 0 0]);


%% EGO WAYPOINTS MATRIX

waypoints = [5 -1.6 0;
    60 -1.6 0;
    150 -1.6 0;
    300 -1.6 0;
    395 -1.6 0];




%% Adaptive Cruise control block parameters

% G_con = tf(1,[0.5,1,0]);        %  Linear model from longitudinal acceleration to longitudinal velocity
% vinit = 20;                     %  Initial condition for longitudinal velocity (m/s)
% D_default = 10;                 %  Default spacing (m)
% vmax = 35;                      %  Maximum velocity (m/s)
% amin = -3;                      %  Minimum longitudinal acceleration (m/s^2)
% amax = 2;                       %  Maximum longitudinal acceleration (m/s^2)
% Prediction_horizon = 30;        %  Prediction horizon (steps)
% Controller_behaivour = 0.5;     %  Controller behavour [More robust 0<----->1 More aggressive]
% vmin = 0;
% 
%%  Multi-Object Tracker
% assigThresh = 30;         % Threshold for assigning detections to tracks
% numTracks = 200;          % Maximum number of tracks
% numSensors = 20;          % Maximum number of sensors
% 
% positionSensor = 1;
% sim(mdl)



%% V2X

% h_T = 1.5;
% h_R = 1.5;
% 
% dF =  (4*h_T*h_R)/lambda;

% sceneOrigin = [-1.8, 4, 0];

P_Signal = 0.2; % in Watts (23 dBm is 0.2 W ; 33dBm is 1.995262315 W)



% logsout = ans.logsout;
% plotMPCACC(logsout,D_default,t_gap,v_set)

%% Simulation parameters

Mode = 1; % Mode [1:4] 1-2/3QAM; 2-3/3QAM; 3-1/2QPSK; 4-3/4QPSK; 5-6 not used
SNRMode = 3; % Different SNR states
RefSpeed = 90/3.6;
RelDistThreshold = 300;
Model = 'V2X_Core_SRI_coding_rate_symbol/To Workspace3';
% SNR0_stat, SNR10_stat, SNR25_stat, SNR25peak300_stat
% SNR0_HV90_d50, SNR10_HV90_d50, SNR25_HV90_d50, SNR25peak300_HV90_d50
% SNR0_HV90_d50, SNR10_HV90_d30, SNR25_HV90_d30, SNR25peak300_HV90_d30


switch Mode
    case 1
        Saving_name = 'SNR25_HV90_d30';
    case 2
        Saving_name = 'SNR25_HV90_d30';
    case 3
        Saving_name = 'SNR25_HV90_d30';
    case 4
        Saving_name = 'SNR25_HV90_d30';
    case 5
        Saving_name = 'SNR0_QAM23_stat_8sym';
    case 6
        Saving_name = 'SNR0_QPKS12_stat_8sym';
end
set_param(Model, 'VariableName', Saving_name);

%%Not_used_parameters

% %% Ego Vehicle parameters
% nrWheelsFr = 2; % Number of wheels on front axle
% nrWheelsRe = 2; % Number of wheels on rear axle
% mEgo = 1500; % Vehicle mass, m [kg]
% a = 1.4; % Longitudinal distance from center of mass to front axle, a [m]
% b = 1.6; % Longitudinal distance from center of mass to rear axle, b [m]
% h = 0.35; % Vertical distance from center of mass to axle plane, h [m]
% 
% Cy_f = 12e3; % Front tire corner stiffness, Cy_f [N/rad]
% Cy_r = 11e3; % Rear tire axle corner stiffness, Cy_r [N/rad]
% sigma_f = 0.1; % Front tire(s) relaxation length, sigma_f [m]
% sigma_r = 0.1; % Rear tire(s) relaxation length, sigma_r [m]
% Izz = 4000; % Yaw polar inertia, Izz [kg*m^2] 
% 
% %% ACTOR IDs
% LeadID = 2;
% InterferingID = 3;
% ThresholdID = 1;
% 
% %% Adaptív tempomat modell
% % mdl = 'V2X_sim.slx';
% % open_system(mdl)
% Ts = 0.1;               %   Sample time
% T = 45;                 %   Stop time
% 
% tau = 0.5;
% m = 2000;
% Fz_f = 1300/m;
% Fz_r = 700/m;
% 
% %% Environment
% 
% Grade = 0;
% WindXYZ = [0 0 0];
% 
% %% Járművek kezdeti értékei:
% 
% a_lead = 2;
% v0_lead = 20;   
% x0_lead = 50;
% 
% v0_con = 30;
% x0_con = 10;
% 
% t_gap = 1.4;
% 
% v_set = 30;