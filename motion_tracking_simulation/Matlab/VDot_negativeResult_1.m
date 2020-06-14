% calculate the maximum value of VDot in a defined neighborhood W.
clear

syms x_o y_o theta_o x_d y_d theta_d x_a y_a theta_a y_diff_da x_diff_da rho alpha alphaStar phi v w rhoDot alphaDot phiDot k1 k2 k3 k4 alphabar l d;

%% derive the formula of alphaStar
x_o = - rho * sin(phi);
y_o = - rho * cos(phi);
theta_o = pi/2 - (alpha + phi);
x_d = 0;
y_d = d;
theta_d = pi/2;
x_a = x_o + l * cos(theta_o);
y_a = y_o + l * sin(theta_o);
theta_a = theta_o;
y_diff_da = y_d - y_a;
x_diff_da = x_d - x_a;
alphaStar = atan2(y_diff_da, x_diff_da) - theta_a

%% control law & kinematics
v = k1*(rho)*cos(alpha);
w = k2*sin(alpha)*cos(alpha) - k3*phi*(sind(alphabar)^2 - sin(alphaStar)^2);

rhoDot = -v*cos(alpha);
alphaDot = v/rho*sin(alpha) - w;
phiDot = - v/rho*sin(alpha);

%% Lyapunov function
V1 = 1/2*rho^2;
V2 = 1/2*sin(alpha)^2;
V3 = 1/2*phi^2;

V1_Dot = diff(V1,rho) * rhoDot;
V2_Dot = diff(V2,alpha) * alphaDot;
V3_Dot = diff(V3,phi) * phiDot;
V_dot = V1_Dot + V2_Dot + V3_Dot;

% V_dot = rho*rhoDot + sin(alpha)*cos(alpha)*alphaDot + phi*phiDot
V_Dot_Simplified = simplify(V_dot);

Rho = linspace(0,1,20);
Alpha= linspace(-pi/6, pi/6, 20);
Phi= linspace(-pi/6, pi/6, 20);
[Rhoo, Alphaa, Phii] = meshgrid(Rho, Alpha, Phi);
% Rhoo = 0.5; Alphaa = -pi/4; Phii = pi/6;

%% calculate the maximum value of VDot...
% V1_Dot = subs(V1_Dot,{k1, k2, k3, rho, alpha, phi, alphabar, l, d}, {0.15, 0.6, 0.82, Rhoo,Alphaa,Phii, 40, 0.1, 0.7});
% size(V1_Dot);
% vpa(V1_Dot,2) ;
% Max = max(V1_Dot(:));
% Max_V1_Dot = vpa(Max,2) 
% 
% V2_Dot = subs(V2_Dot,{k1, k2, k3, rho, alpha, phi, alphabar, l, d}, {0.15, 0.6, 0.82, Rhoo,Alphaa,Phii, 40, 0.1, 0.7});
% size(V2_Dot);
% vpa(V2_Dot,2) ;
% Max = max(V2_Dot(:));
% Max_V2_Dot = vpa(Max,2) 
% 
% V3_Dot = subs(V3_Dot,{k1, k2, k3, rho, alpha, phi, alphabar, l, d}, {0.15, 0.6, 0.82, Rhoo,Alphaa,Phii, 40, 0.1, 0.7});
% size(V3_Dot)
% vpa(V3_Dot,2) ;
% Max = max(V3_Dot(:));
% Max_V3_Dot = vpa(Max,2) 

V_Dot_Simplified_ = subs(V_Dot_Simplified,{k1, k2, k3, rho, alpha, phi, alphabar, l, d}, {0.15, 0.6, 0.82, Rhoo,Alphaa,Phii, 40, 0.1, 0.7});
size(V_Dot_Simplified_)
class(V_Dot_Simplified_)
% vpa(V_Dot_Simplified_,2);
% Max = max(max(max(V_Dot_Simplified_(:,:,:))));
Max = max(V_Dot_Simplified_(:));

% [m,n,p] = find(V_Dot_Simplified_==Max)
A = find(V_Dot_Simplified_(:,:,:)==Max)
Max_V_Dot = vpa(Max,2) 

for i=1:size(V_Dot_Simplified_,1)
    for j=1:size(V_Dot_Simplified_,2)
        for k=1:size(V_Dot_Simplified_,3)
            if V_Dot_Simplified_(i,j,k) == Max
                v=[i j k] %存放a的最大值的三个下标
            end
        end
    end
end
% V_Dot_Simplified_(10,1,20)
vpa(V_Dot_Simplified_(10,1,20),2)
rho_max = Rho(10)
alpha_max = Alpha(1)
phi_max = Phi(20)
clear