clear
rho = linspace(0.5,1,20); % x范围

alpha = linspace(-pi/6, pi/6, 20); % y范围

phi = linspace(-pi/6, pi/6, 20);

% [Rhoo, Alphaa, Phii] = meshgrid(rho, alpha, phi); %构成格点矩阵
[Rhoo, Alphaa] = meshgrid(rho, alpha); %构成格点矩阵


V = Rhoo*0 + Alphaa*0; %计算z的分母，为避免为0，加eps

% scatter3(Rhoo,Alphaa,V,'filled');
surf(Rhoo, Alphaa, V)
title('Surfplot'); %子图1，z绘制三维图形

clear