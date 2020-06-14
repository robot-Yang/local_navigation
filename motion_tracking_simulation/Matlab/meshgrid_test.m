clear
% x = 1:3;
% y = 1:5;
% [X,Y] = meshgrid(x,y)

x = 0:2:6;
y = 0:1:6;
z = 0:3:6;
[X,Y,Z] = meshgrid(x,y,z);
F = X.^2 + Y.^2 + Z.^2;
gridsize = size(F(:))
gridsize = size(F)

max(F)
max(F(:))