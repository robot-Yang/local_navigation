clear

syms x_o y_o theta_o x_d y_d theta_d x_a y_a theta_a y_diff_da x_diff_da rho alpha alphaStar phi v w rhoDot alphaDot phiDot k1 k2 k3 k4 alphabar l d;

% defined limited space W
sam_num = 20;
rho = linspace(0, 2, sam_num);
alpha = linspace(-pi/2, pi/2, sam_num); 
phi = linspace(-pi/2, pi/2, sam_num);
[Rhoo, Alphaa, Phii] = meshgrid(rho, alpha, phi);
size(Rhoo)
size(Alphaa)
size(Phii)

alphaBar = 40;
alphaStar = alpha + phi - pi/2 + atan2(d + l*sin(alpha + phi - pi/2) + rho*cos(phi), rho*sin(phi) - l*cos(alpha + phi - pi/2)) - alphaBar*pi/180;
x0 = solve(alphaStar,k3);
x0