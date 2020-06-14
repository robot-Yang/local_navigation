clear

syms x_o y_o theta_o x_d y_d theta_d x_a y_a theta_a y_diff_da x_diff_da rho alpha alphaStar phi v w rhoDot alphaDot phiDot k1 k2 k3 k4 alphabar l d;


alphabar = 40;
% rho = 1;

alpha = linspace(-pi/6, pi/6, 20); % y范围
phi = linspace(-pi/6, pi/6, 20);

[Alphaa, Phii] = meshgrid(alpha, phi); %构成格点矩阵
% alpha = Alphaa;
% phi = Phii;

x_o = - rho * sin(Phii);
y_o = - rho * cos(Phii);
theta_o = pi/2 - (Alphaa + Phii);
x_d = 0;
y_d = d;
theta_d = pi/2;
x_a = x_o + l * cos(theta_o);
y_a = y_o + l * sin(theta_o);
theta_a = theta_o;
y_diff_da = y_d - y_a;
x_diff_da = x_d - x_a;
alphaStar = atan2(y_diff_da, x_diff_da) - theta_a

size(Alphaa)
size(Phii)
AlphaStar = subs(alphaStar,{rho, alphabar, l, d}, {1, 40, 0.1, 0.7})

vpa(AlphaStar,2) 
size(AlphaStar)

isosurface(Alphaa, Phii, AlphaStar)
title('Surfplot'); %子图1，z绘制三维图形