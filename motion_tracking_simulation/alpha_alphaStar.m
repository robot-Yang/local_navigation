syms OB BC AB BD AD rho alpha alphaStar beta l d;

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
f1=diff(alphaStar,alpha)

% alpha=(-pi/4):(pi/100):(pi/4);
% f3 = abs(asin((sin(alpha + 1/2).*((3*sin(alpha))./(2*sin(alpha + 1/2)) + 3/5))./(((3*sin(1/2))./(2*sin(alpha + 1/2)) - 1/10).^2 + ((3*sin(alpha))./(2*sin(alpha + 1/2)) + 3/5).^2 + cos(alpha + 1/2).*((3*sin(alpha))./(2*sin(alpha + 1/2)) + 3/5).*((3*sin(1/2))./sin(alpha + 1/2) - 1/5)).^(1/2))) - abs(alpha)
% plot(alpha,f3)
clear