syms CD BC AD ACB BCD BD rho l d alpha alphaStar beta;

% CD = d; AB=l; AC=rho;
BC = (l^2 + rho^2 -2*l*rho*cos(alpha))^(1/2);
AD = (d^2 + rho^2 +2*d*rho*cos(beta))^(1/2);
ACB = asin(l*sin(alpha)/BC);
BCD = pi - beta + ACB;
BD = (d^2 + BC^2 -2*d*BC*cos(BCD))^(1/2);
% alphaStar = acos((l^2 + BD^2 - AD^2)/(2*l*BD));
f = alphaStar - acos((l^2 + BD^2 - AD^2)/(2*l*BD));
alpha = solve(f,alpha)
% f1 = subs(f,{rho, beta, l, d},{1.5,0.5,0.1,0.6})


% alpha=(-pi/4):(pi/100):(pi/4);
% f3 = abs(asin((sin(alpha + 1/2).*((3*sin(alpha))./(2*sin(alpha + 1/2)) + 3/5))./(((3*sin(1/2))./(2*sin(alpha + 1/2)) - 1/10).^2 + ((3*sin(alpha))./(2*sin(alpha + 1/2)) + 3/5).^2 + cos(alpha + 1/2).*((3*sin(alpha))./(2*sin(alpha + 1/2)) + 3/5).*((3*sin(1/2))./sin(alpha + 1/2) - 1/5)).^(1/2))) - abs(alpha)
% plot(alpha,f3)
% clear