syms k1 k2 k3 l d alphabar;
% % f(k3) = ((10*k2^2*l)/3 - (10*d*k1^2)/3 - 2*k1*k2 + k1^2 + k2^2 + (25*d^2*k1^2)/9 + (25*k2^2*l^2)/9 - 4*k1*k3*sin((pi*alphabar)/180)^2 + (10*d*k1*k2)/3 - (10*k1*k2*l)/3 + (25*k3^2*l^2*sin((pi*alphabar)/180)^4)/9 + (50*d*k1*k2*l)/9 + (20*d*k1*k3*sin((pi*alphabar)/180)^2)/3 - (10*k1*k3*l*sin((pi*alphabar)/180)^2)/3 + (10*k2*k3*l*sin((pi*alphabar)/180)^2)/3 + (50*k2*k3*l^2*sin((pi*alphabar)/180)^2)/9 + (50*d*k1*k3*l*sin((pi*alphabar)/180)^2)/9)^(1/2)/2 - (5*d*k1)/6 - (5*k2*l)/6 - (5*k3*l*sin((pi*alphabar)/180)^2)/6;
f(k3) = (k1^2 - 2*k1*k2 + k2^2 - 4*k1*k3*sin((pi*alphabar)/180)^2)^(1/2)/2;
x0 = solve(f(k3),k3);
x0
% k1 = 0.5; k2 = 2:
x1 = subs(x0,{k1, k2, alphabar},{0.5,2,40});
x1=eval(x1)
clear

% an:
% k1 = 0.5; k2 = 2; alphabar=40; d=1; l = 0.1;
% x0 = (2*k2^2*l - 2*d*k1^2 - 2*k1*k2 + k1^2 + k2^2 + 2*d*k1*k2 - 2*k1*k2*l)/(4*k1*sin((pi*alphabar)/180)^2 - 4*d*k1*sin((pi*alphabar)/180)^2 + 2*k1*l*sin((pi*alphabar)/180)^2 - 2*k2*l*sin((pi*alphabar)/180)^2);
% k3 = x0;
% k3
% k3 = -((3*d)/2 + 6*l + 9/4)/(2*d*sin((pi*alphabar)/180)^2 + 3*l*sin((pi*alphabar)/180)^2 - 2*sin((pi*alphabar)/180)^2)

% e3 = -(d*k2 + k2*l + k3*l*sin((pi*alphabar)/180)^2)/d; % - k2 - k2*l - k3*l*sin((pi*alphabar)/180)^2

