clear

syms x_o y_o theta_o x_d y_d theta_d x_a y_a theta_a y_diff_da x_diff_da rho alpha alphaStar phi v w rhoDot alphaDot phiDot k1 k2 k3 k4 alphabar l d;

rho = linspace(0.5,1,20);
alpha= linspace(-pi/6, pi/6, 20);
phi= linspace(-pi/6, pi/6, 20);

[Rhoo, Alphaa, Phii] = meshgrid(rho, alpha, phi);

% x_o = - rho * sin(phi);
% y_o = - rho * cos(phi);
% theta_o = pi/2 - (alpha + phi);
% x_d = 0;
% y_d = d;
% theta_d = pi/2;
% x_a = x_o + l * cos(theta_o);
% y_a = y_o + l * sin(theta_o);
% theta_a = theta_o;
% y_diff_da = y_d - y_a;
% x_diff_da = x_d - x_a;
% alphaStar = atan2(y_diff_da, x_diff_da) - theta_a
alphaStar = Alphaa + Phii - pi/2 + atan2(d + Rhoo .* cos(Phii) + l*sin(Alphaa - pi/2 + Phii), Rhoo .* sin(Phii) - l*cos(Alphaa - pi/2 + Phii));

alphabar = 40;
v = k1*(Rhoo)*cos(Alphaa);
w = k2*sin(Alphaa)*cos(Alphaa) - k3*Phii*(sind(alphabar)^2 - sin(alphaStar)^2);

rhoDot = -v*cos(alpha);
alphaDot = v/rho*sin(alpha) - w;
phiDot = - v/rho*sin(alpha);

V1 = 1/2*rho^2;
V2 = 1/2*alpha^2;
V3 = 1/2*phi^2;

V1_Dot = diff(V1,rho) * rhoDot;
V2_Dot = diff(V2,alpha) * alphaDot;
V3_Dot = diff(V3,phi) * phiDot;
V_dot = V1_Dot + V2_Dot + V3_Dot

% V_dot = rho*rhoDot + sin(alpha)*cos(alpha)*alphaDot + phi*phiDot
V_Dot_Simplified = simplify(V_dot)


% 
% V_Dot_Simplified_ = subs(V_Dot_Simplified,{k1, k2, k3, rho, alpha, phi, l, d}, {0.15, 0.6, 0.82, Rho,Alpha,phi, 0.1, 0.7})
% size(V_Dot_Simplified_)
% vpa(V_Dot_Simplified_,2) 
% Max = max(V_Dot_Simplified_)
% vpa(Max,2) 

clear