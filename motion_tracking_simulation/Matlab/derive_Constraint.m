% search the biggest alphaStar in a defined limited space W.

clear

syms x_o y_o theta_o x_d y_d theta_d x_a y_a theta_a y_diff_da x_diff_da rho alpha alphaStar phi v w rhoDot alphaDot phiDot k1 k2 k3 k4 alphabar l d;

% defined limited space W
sam_num = 20;
rho = linspace(0, 2, sam_num);
alpha = linspace(-pi/2, pi/2, sam_num); 
phi = linspace(-pi/2, pi/2, sam_num);
[Rhoo, Alphaa, Phii] = meshgrid(rho, alpha, phi);
size(Rhoo)
size(Alphaa)
size(Phii)

% [Rhoo, Alphaa, Phii] = feasible_space();

% x_o = - Rhoo .* sin(Phii);
% y_o = - Rhoo .* cos(Phii);
% theta_o = pi/2 - (Alphaa + Phii);
% x_d = 0;
% y_d = d;
% theta_d = pi/2;
% x_a = x_o + l * cos(theta_o);
% y_a = y_o + l * sin(theta_o);
% theta_a = theta_o;
% y_diff_da = y_d - y_a;
% x_diff_da = x_d - x_a;
% alphaStar = atan2(y_diff_da, x_diff_da) - theta_a;

alphaStar = Alphaa + Phii - pi/2 + atan2(d + Rhoo .* cos(Phii) + l*sin(Alphaa - pi/2 + Phii), Rhoo .* sin(Phii) - l*cos(Alphaa - pi/2 + Phii));
AlphaStar = subs(alphaStar,{l, d}, {0.1, 0.7});

% figure( 'Name', 'all' )
% p0 = scatter3(Rhoo(:), Alphaa(:), Phii(:));
% legend( p0, 'Sampling point', 'Location', 'NorthEast' );
% xlabel rho(m)
% ylabel alpha
% zlabel phi
% grid on

figure( 'Name', 'left' )
% I = find(AlphaStar < 40*pi/180 & AlphaStar > 38*pi/180);
I = find(AlphaStar < 40*pi/180);
p1 = scatter3(Rhoo(I), Alphaa(I), Phii(I));
legend( p1, 'Sampling point', 'Location', 'NorthEast' );
xlabel rho(m)
ylabel alpha
zlabel phi
grid on



