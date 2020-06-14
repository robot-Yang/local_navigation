function helix()
% 绘制螺旋线 helical line
% 绘制原理：随着时间的延续或z坐标的升高，
% x、y平面上圆的半径不断缩小（指数减小）
t = 0 : 0.01 : pi/4;
x0 = -t.^(0.5).*sin(t);
y0 = -t.^(0.5).*cos(t);

x1 = -2*t.^(0.5).*sin(t);
y1 = -2*t.^(0.5).*cos(t);

x2 = -3*t.^(0.5).*sin(t);
y2 = -3*t.^(0.5).*cos(t);

x3 = -4*t.^(0.5).*sin(t);
y3 = -4*t.^(0.5).*cos(t);

x4 = t.^(0.5).*sin(t);
y4 = -t.^(0.5).*cos(t);

x5 = 2*t.^(0.5).*sin(t);
y5 = -2*t.^(0.5).*cos(t);

x6 = 3*t.^(0.5).*sin(t);
y6 = -3*t.^(0.5).*cos(t);

x7 = 4*t.^(0.5).*sin(t);
y7 = -4*t.^(0.5).*cos(t);

%z = t;
% 绘制二维螺旋线
figure
plot(x0, y0);
hold on;
plot(x1, y1);
hold on;
plot(x2, y2);
hold on;
plot(x3, y3);
hold on;
plot(x4, y4);
hold on;
plot(x5, y5);
hold on;
plot(x6, y6);
hold on;
plot(x7, y7);
hold on;
return