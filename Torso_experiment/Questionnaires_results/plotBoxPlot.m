%% Ploting a BoxPlot of a set of data


function plotBoxPlot(nfig, Data1, LabelsCol, xName, yName,Axes, FigTitle, figPath, RECORD)

    FigureFile = 'epsc';
    FaceALphas = 0.28;
    FontSizes = 36;
    MarkersSizes = 20;
    LinesWidths = 2;
    
    figure(nfig);
    lineWidth = 2; lineCover=3*lineWidth;
    
    boxplot(Data1,LabelsCol); %,'Notch','on');%,'PlotStyle','compact');
     a = [findall(gcf,'Marker','none') findall(gcf,'Marker','.')];
     set(a,'LineWidth',lineWidth,'Marker','.','MarkerSize',lineCover);
    set(gcf, 'name', FigTitle)
    set(gcf, 'Position', [50 20 680 480]);
    set(gca,'FontSize',FontSizes,'LineWidth',LinesWidths)
    set(gca,'FontName','Times New Roman');
    set(gcf,'PaperPositionMode', 'auto');
    xlabel(xName,'FontName','Times New Roman','FontSize',FontSizes);
    ylabel(yName,'FontName','Times New Roman','FontSize',FontSizes);
    axis(Axes);
    title(FigTitle);
    
    if RECORD
        saveas(nfig,strcat(figPath,FigTitle),FigureFile);
    end

end