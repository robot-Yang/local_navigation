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
Axes = [0.5 2.5 0 100];
[p(1),h(1)] =signrank(SUS(:,1),SUS(:,2))
plotBoxPlot(nfig, SUS, LabelsCol, '', 'Score',Axes, string(Tab_names(1)),figPath ,RECORD)
nfig = nfig+1;

%% Godspeed Questionnaire ()
% [p,h,stat] = anova1(anthrop)
Axes = [0.5 2.5 0 4.1];
[p(2),h(2)]=signrank(anthrop(:,1),anthrop(:,2))
plotBoxPlot(nfig, anthrop, LabelsCol, '', 'Score',Axes, string(Tab_names(2)),figPath ,RECORD)
nfig = nfig+1;
%%
Axes = [0.5 2.5 0 4.1];
[p(3),h(3)]=signrank(animacy(:,1),animacy(:,2))
plotBoxPlot(nfig, animacy, LabelsCol, '', 'Score',Axes, string(Tab_names(3)),figPath ,RECORD)
nfig = nfig+1;
%%
Axes = [0.5 2.5 0 4.1];
[p(4),h(4)]=signrank(likeability(:,1),likeability(:,2))
plotBoxPlot(nfig, likeability, LabelsCol, '', 'Score',Axes, string(Tab_names(4)),figPath ,RECORD)
nfig = nfig+1;
%%
Axes = [0.5 2.5 0 4.1];
[p(5),h(5)]=signrank(intelligence(:,1),intelligence(:,2))
plotBoxPlot(nfig, intelligence, LabelsCol, '', 'Score',Axes, string(Tab_names(5)),figPath ,RECORD)
nfig = nfig+1;
%%
Axes = [0.5 2.5 0 4.1];
[p(6),h(6)]=signrank(safety(:,1),safety(:,2))
plotBoxPlot(nfig, safety, LabelsCol, '', 'Score',Axes, string(Tab_names(6)),figPath ,RECORD)
nfig = nfig+1;



