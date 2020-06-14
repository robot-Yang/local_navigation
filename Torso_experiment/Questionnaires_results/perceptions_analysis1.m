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

%%     System Usability Score (SUS)
% [p,h,stat] = anova1(SUS)
% Axes = [0.5 2.5 0 100];
% [p(1),h(1)] =signrank(SUS(:,1),SUS(:,2))
% plotBoxPlot(nfig, SUS, LabelsCol, '', 'Score',Axes, string(Tab_names(1)),figPath ,RECORD)
% nfig = nfig+1;

boxplot(SUS);
nfig = nfig+1;
% boxplot(anthrop);
% nfig = nfig+1;



