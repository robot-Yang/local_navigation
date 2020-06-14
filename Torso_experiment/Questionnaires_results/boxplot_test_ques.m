%%  Meta Analysis of experimental results
% Created : Nov. 1st, 2019
% Author: Diego F. Paez G.

clc 
clear all
close all

 if ismac
       % addpath('../../General_Functions/');
        figPath = ('Figures');
    else
        %addpath('..\..\General_Functions\');
        figPath = ('Figures');
 end
 
    RECORD = 1;
    nfig=1;
    FaceALphas = 0.18;
    FontSizes = 28;
    MarkersSizes = 14;
    LinesWidths = 3;
    FigureFile = 'epsc';
    Fonts = 'Times New Roman';
    
%     load questionnaire.dat
    questionnaire()
        Tab_names = {...
        'SUS'
        'Anthropomorphism'
        'Animacy'
        'Likeability'
        'Perceived Intelligence'
        'Perceived safety'};
LabelsCol = {'Torso' 'Joystick'};
%% 
DeviceColors = {'r' 'g'};

GroupedData = {SUS anthrop animacy likeability intelligence safety}; 


disp('SUS is:')
disp(SUS)
size(SUS)

N = numel(GroupedData);
delta = linspace(-.3,.3,N); %// define offsets to distinguish plots
width = .2; %// small width to avoid overlap
cmap = hsv(N); %// colormap
legWidth = 1.8; %// make room for legend

figure;
hold on;

disp(N)

for ii=1:2
    labels = Tab_names; 
    disp(labels)
    disp('position')
    disp((1:numel(labels))+delta(ii))
    boxplot(GroupedData{ii},'Color', DeviceColors{ii}, 'boxstyle','filled', ...
        'position',(1:numel(labels))+delta(ii), 'widths',width, 'labels',labels)
        
    plot(NaN,1,'color',DeviceColors{ii}); %// dummy plot for legend
end

xlabel('Speed'); ylabel('Step Count'); grid on;
xlim([1+2*delta(1) numel(labels)+legWidth+2*delta(N)]) %// adjust x limits, with room for legend

legend(LabelsCol);
