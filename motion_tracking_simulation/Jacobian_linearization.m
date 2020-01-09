%% original forklift's kinematics from paper, linearization on (0,0,0)
% syms rho alpha beta delta v1 v2 v3 rhoDot alphaDot betaDot k1 k2 k3 l alphabar;
% 
% v1 = k1*(rho)*cos(alpha);
% v2 = -l * (k2*sin(alpha)*cos(alpha) - k3*beta*(sind(alphabar)^2 - sin(alpha)^2));
% 
% v = sign(v1) * (v1^2 + v2^2)^(1/2); %  
% delta = atan(v2/v1);
% 
% rhoDot = -v*cos(alpha)*cos(delta);
% alphaDot = v/(rho)*sin(alpha)*cos(delta) + v/l*sin(delta);
% betaDot = - v/(rho)*sin(alpha)*cos(delta);

% J = jacobian([rhoDot;alphaDot;betaDot],[rho alpha beta]); % obtain jacobian matrix
% J
% J1 = subs(J,{rho, alpha, beta},{0,0,0}) % linearization on (0,0,0)
% e = eig(J1) % obtain eigenvalues
% clear

%% forklift's kinematics from paper, linearization on (0,0,0)
% syms rho alpha beta delta v1 v2 v3 rhoDot alphaDot betaDot k1 k2 k3 l alphabar;
% 
% rhoDot = -k1*rho*cos(alpha)^2;
% alphaDot = -(k2-k1)*sin(alpha)*cos(alpha) + k1*k3*beta*(sin(alphabar)^2 - sin(alpha)^2);
% betaDot = -k1*sin(alpha)*cos(alpha);
% 
% J = jacobian([rhoDot;alphaDot;betaDot],[rho alpha beta]); % obtain jacobian matrix
% J
% J1 = subs(J,{rho, alpha, beta},{0,0,0}) % linearization on (0,0,0)
% e = eig(J1) % obtain eigenvalues
% clear 

%% Qolo's kinematics on camera (from chair to camera), linearization on (d,0,0)
% syms rho alpha beta v w rhoDot alphaDot betaDot k1 k2 k3 l d alphabar;
% 
% v = k1*(rho-d)*cos(alpha)*cos(beta);
% w = k2*sin(alpha)*cos(alpha) - k3*beta*(sind(alphabar)^2 - sin(alpha)^2);
% 
% rhoDot = - v*cos(alpha) - w*l*sin(alpha);
% alphaDot = v/rho*sin(alpha) - w*(l/rho*cos(alpha) + 1);
% betaDot = - v/rho*sin(alpha) + w*(l/rho*cos(alpha));
% 
% J = jacobian([rhoDot;alphaDot;betaDot],[rho alpha beta]);
% J
% J1 = subs(J,{rho, alpha, beta},{d,0,0})
% e = eig(J1)
% clear

%% Qolo's kinematics 6 components, linearization on (d,0,0)
% syms rho alpha beta rhoStar alphaStar betaStar v w rhoDot alphaDot betaDot rhoStarDot alphaStarDot betaStarDot k1 k2 k3 l d alphabar;
% 
% % v = k1*(rho)*cos(alpha);
% % w = k2*sin(alpha)*cos(alpha) - k3*beta*(sind(alphabar)^2 - sin(alphaStar)^2);
% 
% v = k1*(rho)*cos(alpha);
% w = k2*sin(alpha)*cos(alpha) - k3*beta*(sind(alphabar)^2 - sin(alphaStar)^2);
% 
% rhoDot = -v*cos(alpha);
% alphaDot = v/rho*sin(alpha) - w;
% betaDot = - v/rho*sin(alpha);
% 
% rhoStarDot = - v*cos(alphaStar) - w*l*sin(alphaStar);
% alphaStarDot = v/rhoStar*sin(alphaStar) - w*(l/rhoStar*cos(alphaStar) + 1);
% betaStarDot = - v/rhoStar*sin(alphaStar) + w*(l/rhoStar*cos(alphaStar));
% 
% J = jacobian([rhoDot;alphaDot;betaDot;rhoStarDot;alphaStarDot;betaStarDot],[rho alpha beta rhoStar alphaStar betaStar]);
% J
% J1 = subs(J,{rho, alpha, beta, rhoStar, alphaStar, betaStar},{0,0,0,d,0,0})
% e = eig(J1)
% clear

%% Qolo's kinematics on camera (no attractor), linearization on (0,0,0)
% syms rho alpha beta v w rhoDot alphaDot betaDot k1 k2 k3 l alphabar;
% 
% v = k1*(rho)*cos(alpha);
% w = k2*sin(alpha)*cos(alpha) - k3*beta*(sind(alphabar)^2 - sin(alpha)^2);
% 
% rhoDot = -v*cos(alpha) - w*l*sin(alpha);
% alphaDot = v/rho*sin(alpha) - w*(l/rho*cos(alpha) + 1);
% betaDot = - v/rho*sin(alpha) + w*(l/rho*cos(alpha));
% 
% J = jacobian([rhoDot;alphaDot;betaDot],[rho alpha beta]);
% J
% J1 = subs(J,{rho, alpha, beta},{0,0,0})
% e = eig(J1)
% clear

%% Qolo's kinematics on center (from attractor to center), linearization on (0,0,0)
% syms rho alpha beta v w rhoDot alphaDot betaDot k1 k2 k3 alphabar;
% 
% v = k1*(rho)*cos(alpha);
% w = k2*sin(alpha)*cos(alpha) - k3*beta*(sind(alphabar)^2 - sin(alpha)^2);
% 
% rhoDot = -v*cos(alpha);
% alphaDot = v/rho*sin(alpha) - w;
% betaDot = - v/rho*sin(alpha);
% 
% J = jacobian([rhoDot;alphaDot;betaDot],[rho alpha beta]);
% J
% J1 = subs(J,{rho, alpha, beta},{0,0,0})
% e = eig(J1)
% clear

%% Qolo's kinematics on center (from attractor to center), replace alpha with alphaStar, linearization on (0,0,0)
% syms OB BC AB BD AD P rho alpha alphaStar beta v w rhoDot alphaDot betaDot k1 k2 k3 alphabar l d;
% 
% % kk = sign(alpha*beta);
% OB = rho * sin(beta) / sin(pi-alpha-beta);
% BC = rho * sin(alpha) / sin(pi-alpha-beta);
% AB = OB - l;
% BD = BC + d;
% AD = AB^2 + BD^2 - 2*AB*BD*cos(pi-alpha-beta);
% alphaStar = asin(BD*sin(pi-alpha-beta) / AD);
% % P = BD*sin(pi-alpha-beta);
% % alphaStar = atan2(P / (AD^2 - P^2)^(1/2));
% 
% v = k1*(rho)*cos(alpha);
% w = k2*sin(alpha)*cos(alpha) - k3*beta*(sind(alphabar)^2 - sin(alphaStar)^2);
% 
% rhoDot = -v*cos(alpha);
% alphaDot = v/rho*sin(alpha) - w;
% betaDot = - v/rho*sin(alpha);
% 
% J = jacobian([rhoDot;alphaDot;betaDot],[rho alpha beta]);
% J
% % J1 = subs(J,{rho, alpha, beta},{0,0,0})
% % e = eig(J1)
% 
% % V1 = 1/2*rho^2;
% % V2 = 1/2*alpha;
% % V3 = 1/2*beta^2;
% 
% % V1_Dot = diff(V1,rho);
% % V2_Dot = diff(V2,alpha);
% % V3_Dot = diff(V3,beta);
% % V_dot = V1_Dot + V2_Dot + V3_Dot;
% 
% % V_dot = rho*rhoDot + alpha*alphaDot + beta*betaDot
% % V_Dot_Simplified = simplify(V_dot)
% % 
% % Rho = 0.01:0.01:1.5;
% % Alpha= 0.01:0.01:1.5;
% % Beta= 0.01:0.01:1.5;
% % V_Dot_Simplified_ = subs(J,{rho, alpha, beta},{Rho,Alpha,Beta})

%% Qolo's kinematics on center (from attractor to center), replace alpha with alphaStar, linearization on (0,0,0)
clear
syms x_o y_o theta_o x_d y_d theta_d x_a y_a theta_a y_diff_da x_diff_da rho alpha alphaStar beta v w rhoDot alphaDot betaDot k1 k2 k3 alphabar l d;

% l = 0.1
% d = 0.7

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

v = k1*(rho)*cos(alpha)*cos(alphaStar - alphabar*pi/180 + pi/2);
w = k2*alpha + k3*beta*(sind(alphabar)^2 - sin(alphaStar)^2);

rhoDot = -v*cos(alpha);
alphaDot = v/rho*sin(alpha) - w;
betaDot = - v/rho*sin(alpha);

V1 = 1/2*rho^2;
V2 = 1/2*alpha;
V3 = 1/2*beta^2;

V1_Dot = diff(V1,rho);
V2_Dot = diff(V2,alpha);
V3_Dot = diff(V3,beta);
V_dot = V1_Dot + V2_Dot + V3_Dot;

J = jacobian([rhoDot;alphaDot;betaDot],[rho alpha beta]);
J
J1 = subs(J,{rho, alpha, beta},{0,0,0})
J2 = subs(J1, {l, d}, {0.1, 0.7})
e = eig(J2)
e = simplify(e)

% ff = k1^2*sin((pi*alphabar)/180)^2 + k2^2 + 4*k1*k3*sin((pi*alphabar)/180)^3 - 2*k1*k2*sin((pi*alphabar)/180)
% 4*k1*k3*sin((pi*alphabar)/180)^3 - 2*k1*k2*sin((pi*alphabar)/180);
% fff = solve(ff,k3);
% Ans = subs(fff,{k1,k2,alphabar},{0.15,0.6,40});
% vpa(Ans)
%% Qolo's kinematics on center (from attractor to center), replace alpha with alphaStar, linearization on (0,0,0)
clear
syms x_o y_o theta_o x_d y_d theta_d x_a y_a theta_a y_diff_da x_diff_da rho alpha alphaStar beta v w rhoDot alphaDot betaDot k1 k2 k3 alphabar l d;

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

v = k1*(rho)*cos(alpha);
w = k2*sin(alpha)*cos(alpha) + k3*beta*(sind(alphabar)^2 - sin(alphaStar)^2);

rhoDot = -v*cos(alpha);
alphaDot = v/rho*sin(alpha) - w;
betaDot = - v/rho*sin(alpha);

J = jacobian([rhoDot;alphaDot;betaDot],[rho alpha beta]);
J
J1 = subs(J,{rho, alpha, beta},{0,0,0})
J2 = subs(J1, {l, d}, {0.1, 0.7})
e = eig(J2)
% e = simplify(e)

% ff = k1^2 - 2*k1*k2 + k2^2 + 4*k1*k3*sin((pi*alphabar)/180)^2
% 4*k1*k3*sin((pi*alphabar)/180)^3 - 2*k1*k2*sin((pi*alphabar)/180);
% fff = solve(ff,k3);
% Ans = subs(fff,{k1,k2,alphabar},{0.15,0.6,40});
% vpa(Ans)
%% rho change
% syms rho alpha beta v w rhoDot alphaDot betaDot k1 k2 k3 l d alphabar;
% 
% rhoStar = (rho^2+d^2 - 2*rho*d*cos(beta))^(1/2)
% cosA = (rhoStar^2 + d^2 - rho^2) / (2*rhoStar*d)
% 
% v = sign(-cosA)*k1*(rhoStar)*cos(alpha);
% w = k2*sin(alpha)*cos(alpha) - k3*beta*(sind(alphabar)^2 - sin(alpha)^2);
% 
% rhoDot = -v*cos(alpha) - w*l*sin(alpha);
% alphaDot = v/rho*sin(alpha) - w*(l/rho*cos(alpha) + 1);
% betaDot = - v/rho*sin(alpha) + w*(l/rho*cos(alpha));
% 
% J = jacobian([rhoDot;alphaDot;betaDot],[rho alpha beta]);
% J
% J1 = subs(J,{rho, alpha, beta},{0,0,0})
% e = eig(J1)
% clear