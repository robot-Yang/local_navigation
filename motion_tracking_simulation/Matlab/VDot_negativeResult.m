clear

syms x_o y_o theta_o x_d y_d theta_d x_a y_a theta_a y_diff_da x_diff_da rho alpha alphaStar beta v w rhoDot alphaDot betaDot k1 k2 k3 k4 alphabar l d;

x_o = - rho * sin(beta);
y_o = - rho * cos(beta);
theta_o = pi/2 - (alpha + beta);
x_d = 0;
y_d = d;
theta_d = pi/2;
x_a = x_o + l * cos(theta_o);
y_a = y_o + l * sin(theta_o);
theta_a = theta_o;
y_diff_da = y_d - y_a;
x_diff_da = x_d - x_a;
alphaStar = atan2(y_diff_da, x_diff_da) - theta_a

alphabar = 40;
v = k1*(rho)*cos(alpha);
w = k2*sin(alpha)*cos(alpha) - k3*beta*(sind(alphabar)^2 - sin(alphaStar)^2);

rhoDot = -v*cos(alpha);
alphaDot = v/rho*sin(alpha) - w;
betaDot = - v/rho*sin(alpha);

V1 = 1/2*rho^2;
V2 = 1/2*alpha^2;
V3 = 1/2*beta^2;

% V1_Dot = diff(V1,rho);
% V2_Dot = diff(V2,alpha);
% V3_Dot = diff(V3,beta);
% V_dot = V1_Dot + V2_Dot + V3_Dot

V_dot = rho*rhoDot + sin(alpha)*cos(alpha)*alphaDot + beta*betaDot
V_Dot_Simplified = simplify(V_dot)

Rho = linspace(0.5,1,20);
Alpha= linspace(-pi/6, pi/6, 20);
Beta= linspace(-pi/6, pi/6, 20);

V_Dot_Simplified_ = subs(V_Dot_Simplified,{k1, k2, k3, rho, alpha, beta, l, d}, {0.15, 0.6, 0.82, Rho,Alpha,Beta, 0.1, 0.7})
vpa(V_Dot_Simplified_,2) 
Max = max(V_Dot_Simplified_)
vpa(Max,2) 

clear