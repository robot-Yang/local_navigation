% [X,Y,Z]=peaks(30);
% R=sqrt(X.^2+Y.^2);
% 
% surf(X,Y,Z,R);
% axis tight  

clear
X = linspace(0.5,1,20); % x范围

Y = linspace(-pi/6, pi/6, 20); % y范围

Z = linspace(-pi/6, pi/6, 20);

[XX,YY,ZZ] = meshgrid(X,Y,Z);
ZZZ = sin(XX) + cos(YY);
surf(XX,YY,ZZZ)

clear