%% kinematics on camera (from chair to camera)
% 
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
%% rho change
syms rho alpha beta v w rhoDot alphaDot betaDot k1 k2 k3 l d alphabar;

v = k1*((rho^2+d^2 - 2*rho*d*cos(beta))^(1/2))*cos(alpha);
w = k2*sin(alpha)*cos(alpha) - k3*beta*(sind(alphabar)^2 - sin(alpha)^2);

rhoDot = -v*cos(alpha) - w*l*sin(alpha);
alphaDot = v/rho*sin(alpha) - w*(l/rho*cos(alpha) + 1);
betaDot = - v/rho*sin(alpha) + w*(l/rho*cos(alpha));

J = jacobian([rhoDot;alphaDot;betaDot],[rho alpha beta]);
J
%% rho_x, rho_y
% syms rho rho_x rho_y alpha beta v w rhoDot alphaDot betaDot k1 k2 k3 l d alphabar;
% 
% rho = (rho_x^2 + rho_y^2) ^ (1/2);
% rhoStar_x = rho_x + d * sin(beta + alpha);
% rhoStar_y = rho_x - d * cos(beta + alpha);
% 
% v = k1*(rhoStar_x^2 + rhoStar_y^2)^(1/2)*cos(alpha);
% w = k2*sin(alpha)*cos(alpha) - k3*beta*(sind(alphabar)^2 - sin(alpha)^2);
% 
% rho_xDot = w*l;
% rho_yDot = -v;
% alphaDot = v/rho*sin(alpha) - w*(l/rho*cos(alpha) + 1);
% betaDot = - v/rho*sin(alpha) + w*(l/rho*cos(alpha));
% 
% J = jacobian([rho_xDot;rho_yDot;alphaDot;betaDot],[rho_x rho_y alpha beta]);
% J
% e = eig(J)
%% original kinematics on Qolo center
syms rho alpha beta v w rhoDot alphaDot betaDot k1 k2 k3 l d alphabar;

v = k1*(rho)*cos(alpha);
w = k2*sin(alpha)*cos(alpha) - k3*beta*(sind(alphabar)^2 - sin(alpha)^2);

rhoDot = -v*cos(alpha) - w*l*sin(alpha);
alphaDot = v/(rho)*sin(alpha) - w*(l/(rho)*cos(alpha) + 1);
betaDot = - v/(rho)*sin(alpha) + w*(l/(rho)*cos(alpha));

J = jacobian([rhoDot;alphaDot;betaDot],[rho alpha beta]);
J
%% original kinematics on Qolo center
% syms rho alpha beta v w rhoDot alphaDot betaDot k1 k2 k3 l d alphabar;
% 
% v = k1*(rho)*cos(alpha);
% w = k2*sin(alpha)*cos(alpha) - k3*beta*(sind(alphabar)^2 - sin(alpha)^2);
% 
% rhoDot = -v*cos(alpha) - w*l*sin(alpha);
% alphaDot = v/(rho-v*cos(alpha))*sin(alpha) - w*(l/(rho-w*l*sin(alpha))*cos(alpha) + 1);
% betaDot = - v/(rho-v*cos(alpha))*sin(alpha) + w*(l/(rho-w*l*sin(alpha))*cos(alpha));
% 
% J = jacobian([rhoDot;alphaDot;betaDot],[rho alpha beta]);
% J
%% 11 %% original kinematics from paper
% syms rho alpha beta delta v1 v2 v3 rhoDot alphaDot betaDot k1 k2 k3 l alphabar;
% 
% v1 = k1*(rho)*cos(alpha);
% v2 = -l * (k2*sin(alpha)*cos(alpha) - k3*beta*(sind(alphabar)^2 - sin(alpha)^2));
% 
% v = (v1^2 + v2^2)^(1/2); % sign(v1) * 
% delta = atan(v2/v1);
% 
% rhoDot = -v*cos(alpha)*cos(delta);
% alphaDot = v/(rho)*sin(alpha)*cos(delta) + v/l*sin(delta);
% betaDot = - v/(rho)*sin(alpha)*cos(delta);
% 
% J = jacobian([rhoDot;alphaDot;betaDot],[rho alpha beta]);
% J

