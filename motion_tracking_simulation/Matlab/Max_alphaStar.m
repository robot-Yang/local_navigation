% search the biggest alphaStar in a defined limited space W.

clear

syms x_o y_o theta_o x_d y_d theta_d x_a y_a theta_a y_diff_da x_diff_da rho alpha alphaStar phi v w rhoDot alphaDot phiDot k1 k2 k3 k4 alphabar l d;

% defined limited space W
% rho = linspace(0, 1, 40);
% alpha = linspace(-pi/5, pi/5, 20); 
% phi = linspace(-pi/6, pi/6, 20);
% [Rhoo, Alphaa, Phii] = meshgrid(rho, alpha, phi);

[Rhoo, Alphaa, Phii] = feasible_space();

% x_o = - Rhoo .* sin(Phii);
% y_o = - Rhoo .* cos(Phii);
% theta_o = pi/2 - (Alphaa + Phii);
% x_d = 0;
% y_d = d;
% theta_d = pi/2;
% x_a = x_o + l * cos(theta_o);
% y_a = y_o + l * sin(theta_o);
% theta_a = theta_o;
% y_diff_da = y_d - y_a;
% x_diff_da = x_d - x_a;
% alphaStar = atan2(y_diff_da, x_diff_da) - theta_a;

alphaStar = Alphaa + Phii - pi/2 + atan2(d + Rhoo .* cos(Phii) + l*sin(Alphaa - pi/2 + Phii), Rhoo .* sin(Phii) - l*cos(Alphaa - pi/2 + Phii));
AlphaStar = subs(alphaStar,{l, d}, {0.1, 0.7});

% vpa(AlphaStar,2);
% size(AlphaStar(:))
size(AlphaStar)

Max = max(AlphaStar(:))
vpa(Max*180/pi,2) 

% [xm,ym,zm]=find(Max==AlphaStar)
