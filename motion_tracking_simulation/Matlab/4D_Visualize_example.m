x=-8:0.5:8; % x范围

y=-8:0.5:8; % y范围

[xx,yy]=meshgrid(x,y); %构成格点矩阵

c=sqrt(xx.^2+yy.^2)+eps; %计算z的分母，为避免为0，加eps

z=sin(c)./c; %计算z

subplot(2,2,1)

surf(xx,yy,z);title('Surfplot'); %子图1，绘制三维图形

subplot(2,2,2)

mesh(xx,yy,z);title('Meshplot'); %子图2，绘制三维曲面

subplot(2,2,3)

surf(xx,yy,z);title('Surplot with shading interp'); %子图3，绘制三维曲面，表面为光滑

shading interp;

subplot(2,2,4)

contour(xx,yy,z);title('Meshplot'); %子图4，绘制等高曲线