syms OB BC AB BD AD rho alpha alphaStar beta l d;

OB = rho * sin(beta) / sin(pi-alpha-beta);
BC = rho * sin(alpha) / sin(pi-alpha-beta);
AB = OB - l;
BD = BC + d;
AD = (AB^2 + BD^2 - 2*AB*BD*cos(pi-alpha-beta))^(1/2);
alphaStar = asin(BD*sin(pi-alpha-beta) / AD);
f = abs(alphaStar) - abs(alpha);
f1 = subs(f,{rho, beta, l, d},{1.5,0.5,0.1,0.6})
% f2 = subs(f1,{alpha},{0.5})
% f2=eval(f2)
% OB = subs(OB,{rho, alpha, beta},{1.5,0.5,0.5})
% OB=eval(OB)
% BC = subs(BC,{rho, alpha, beta},{1.5,0.5,0.5})
% BC=eval(BC)
% AD = subs(AD,{rho, alpha, beta,l,d},{1.5,0.5,0.5,0.1,0.6})
% AD=eval(AD)
% alphaStar = subs(alphaStar,{rho, alpha, beta,l,d},{1.5,0.5,0.5,0.1,0.6})
% alphaStar=eval(alphaStar)
% sin(0.5)
% sin(1)
% clear
% alpha=-pi/4:pi/100:pi/4;
% f2 = f1
% plot(alpha,f2)

alpha=(-pi/4):(pi/100):(pi/4);
% f = asin((sin(alpha + 1/2).*((3*sin(alpha))./(2*sin(alpha + 1/2)) + 3/5))./(((3*sin(1/2))./(2*sin(alpha + 1/2)) - 1/10).^2 + ((3*sin(alpha))/(2*sin(alpha + 1/2)) + 3/5).^2 + cos(alpha + 1/2).*((3*sin(alpha))./(2*sin(alpha + 1/2)) + 3/5).*((3*sin(1/2))./sin(alpha + 1/2) - 1/5))) - alpha;
f3 = abs(asin((sin(alpha + 1/2).*((3*sin(alpha))./(2*sin(alpha + 1/2)) + 3/5))./(((3*sin(1/2))./(2*sin(alpha + 1/2)) - 1/10).^2 + ((3*sin(alpha))./(2*sin(alpha + 1/2)) + 3/5).^2 + cos(alpha + 1/2).*((3*sin(alpha))./(2*sin(alpha + 1/2)) + 3/5).*((3*sin(1/2))./sin(alpha + 1/2) - 1/5)).^(1/2))) - abs(alpha)
plot(alpha,f3)
clear