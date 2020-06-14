% rho: camera to Destination
% alphaStar: camera to Center of Chair
% beta: camera to Center of Chair
% no alpha

syms OB BC AB BD AD rho alpha alphaStar beta l d;
syms k1 v w rho_Dot alpha_Dot beta_Dot alphaBar;

OB = rho * sin(beta) / sin(pi-alpha-beta);
BC = rho * sin(alpha) / sin(pi-alpha-beta);
AB = OB - l;
BD = BC + d;
AD = (AB^2 + BD^2 - 2*AB*BD*cos(pi-alpha-beta))^(1/2);
% f = BD*sin(pi-alpha-beta) - sin(alphaStar) * AD;
alphaStar = asin(BD*sin(pi-alpha-beta) / AD)
% f = alphaStar - asin(BD*sin(pi-alpha-beta) / AD);
% alphaStar = solve(f,alphaStar)
% f1 = subs(f,{rho, beta, l, d},{1.5,0.5,0.1,0.6})
alphaStar_Dotrho = diff(alphaStar,rho)
alphaStar_Dotalpha = diff(alphaStar,alpha)
alphaStar_Dotbeta = diff(alphaStar,beta)


% alpha=(-pi/4):(pi/100):(pi/4);
% f3 = abs(asin((sin(alpha + 1/2).*((3*sin(alpha))./(2*sin(alpha + 1/2)) + 3/5))./(((3*sin(1/2))./(2*sin(alpha + 1/2)) - 1/10).^2 + ((3*sin(alpha))./(2*sin(alpha + 1/2)) + 3/5).^2 + cos(alpha + 1/2).*((3*sin(alpha))./(2*sin(alpha + 1/2)) + 3/5).*((3*sin(1/2))./sin(alpha + 1/2) - 1/5)).^(1/2))) - abs(alpha)
% plot(alpha,f3)

v = k1 * rho * cos(alpha);
% w = w;

rho_Dot = -v * cos(alpha);
alpha_Dot = (v/rho) * sin(alpha) + w;
beta_Dot = -(v/rho) * sin(alpha);

alphaStar_Dot = alphaStar_Dotrho * rho_Dot + alphaStar_Dotalpha * alpha_Dot + alphaStar_Dotbeta * beta_Dot

% V1 = 1/2*rho^2;
% V2 = 1/2*log(sin(alphaBar)^2/(sin(alphaBar)^2 - sin(alphaStar)^2));
% V3 = 1/2*alpha^2;
% 
% V = V1 + V2 + V3;
% f2 = diff(V1,alpha);

% V_Dot = -k1*rho^2*cos(alpha)^2 - k1*sin(alpha)*cos(alpha)*beta + sin(alphaStar)*cos(alphaStar)/(sin(alphaBar)^2 - sin(alphaStar)^2) * alphaStar_Dot;
% f2 = solve(V_Dot,w)
f2 = simplify(alphaStar_Dot)
clear