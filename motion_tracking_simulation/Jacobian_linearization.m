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
% v = k1*(rho-d)*cos(alpha);
% w = k2*sin(alpha)*cos(alpha) - k3*beta*(sind(alphabar)^2 - sin(alpha)^2);
% 
% rhoDot = -v*cos(alpha) - w*l*sin(alpha);
% alphaDot = v/rho*sin(alpha) - w*(l/rho*cos(alpha) + 1);
% betaDot = - v/rho*sin(alpha) + w*(l/rho*cos(alpha));
% 
% J = jacobian([rhoDot;alphaDot;betaDot],[rho alpha beta]);
% J
% J1 = subs(J,rho, alpha, beta},{d,0,0})
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
syms OB BC AB BD AD rho alpha alphaStar beta v w rhoDot alphaDot betaDot k1 k2 k3 alphabar l d;

% kk = sign(alpha*beta);
OB = rho * sin(beta) / sin(pi-alpha-beta);
BC = rho * sin(alpha) / sin(pi-alpha-beta);
AB = OB - l;
BD = BC + d;
AD = AB^2 + BD^2 - 2*AB*BD*cos(pi-alpha-beta);
alphaStar = asin(BD*sin(pi-alpha-beta) / AD);
% P = BD*sin(pi-alpha-beta);
% alphaStar = atan2(P / (AD^2 - P^2)^(1/2));

v = k1*(rho)*cos(alpha);
w = k2*sin(alpha)*cos(alpha) - k1*k3*beta*(sind(alphabar)^2 - sin(alphaStar)^2);

rhoDot = -v*cos(alpha);
alphaDot = v/rho*sin(alpha) - w;
betaDot = - v/rho*sin(alpha);

J = jacobian([rhoDot;alphaDot;betaDot],[rho alpha beta]);
J
J1 = subs(J,{rho, alpha, beta},{0,0,0})
e = eig(J1)


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