% this program is used to calculate the maximum value of a binary function
%-----written by  Dr.Liao,  Aug 25th  2018, SLCOE OF DUT
tic
clear all
close all
clc

deta=0.01;

x=0.1:deta:0.4;
y=0.1:deta:0.4;

mm=length(x);
nn=length(y);

z=zeros(mm,nn);

for i=1:mm
     for j=1:nn
     
     
     z(i,j)=(-0.2323*x(i)^2+0.2866*x(j)^2)*(0.2323*x(i)^2-0.2866*x(j)^2+2*(-0.5406)*0.1^2+1.0203*0.1^2*x(i)^2/((x(i)^2+x(j)^2)^0.5*tanh(2*(x(i)^2+x(j)^2)^0.5)-x(i)^2*(0.5733-0)^2));
                              
     end
     
     
end

z_m=max(max(z)),
[row,col]=find(z_m==z),
xm=x(1,row)
ym=y(1,col)

%--------------------------------------------
syms x1 x2;
y=(-0.2323*x1^2+0.2866^2*x2^2)*(0.2323*x1^2-0.2866*x2^2+2*(-0.5406)*0.1^2+1.0203*0.1^2*x1^2/((x1^2+x2^2)^0.5*tanh(2*(x1^2+x2^2)^0.5)-x1^2*(0.5733-0)^2));;
ezsurf(y,[0.1 0.4],[0.1 0.4]);
     
     



toc