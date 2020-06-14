% e =
%  
%                                                                                                                                                                                                                                                                                   -k1
%     (k1*abs(d*1i - l*1i) - k2*abs(d*1i - l*1i) + (k1^2*abs(d*1i - l*1i)^2 + k2^2*abs(d*1i - l*1i)^2 + 4*k1*k3*imag(d)^2 + 4*k1*k3*imag(l)^2 - 2*k1*k2*abs(d*1i - l*1i)^2 - 8*k1*k3*imag(d)*imag(l) - 4*k1*k3*abs(d*1i - l*1i)^2*sin((pi*alphabar)/180)^2)^(1/2))/(2*abs(d*1i - l*1i))
%  -(- k1*abs(d*1i - l*1i) + k2*abs(d*1i - l*1i) + (k1^2*abs(d*1i - l*1i)^2 + k2^2*abs(d*1i - l*1i)^2 + 4*k1*k3*imag(d)^2 + 4*k1*k3*imag(l)^2 - 2*k1*k2*abs(d*1i - l*1i)^2 - 8*k1*k3*imag(d)*imag(l) - 4*k1*k3*abs(d*1i - l*1i)^2*sin((pi*alphabar)/180)^2)^(1/2))/(2*abs(d*1i - l*1i))

syms k1 k2 k3
e0 = -k1;
e1 = (k1*abs(d*1i - l*1i) - k2*abs(d*1i - l*1i) + (k1^2*abs(d*1i - l*1i)^2 + k2^2*abs(d*1i - l*1i)^2 + 4*k1*k3*imag(d)^2 + 4*k1*k3*imag(l)^2 - 2*k1*k2*abs(d*1i - l*1i)^2 - 8*k1*k3*imag(d)*imag(l) - 4*k1*k3*abs(d*1i - l*1i)^2*sin((pi*alphabar)/180)^2)^(1/2))/(2*abs(d*1i - l*1i));
e2 = -(- k1*abs(d*1i - l*1i) + k2*abs(d*1i - l*1i) + (k1^2*abs(d*1i - l*1i)^2 + k2^2*abs(d*1i - l*1i)^2 + 4*k1*k3*imag(d)^2 + 4*k1*k3*imag(l)^2 - 2*k1*k2*abs(d*1i - l*1i)^2 - 8*k1*k3*imag(d)*imag(l) - 4*k1*k3*abs(d*1i - l*1i)^2*sin((pi*alphabar)/180)^2)^(1/2))/(2*abs(d*1i - l*1i));
e1 - e2
clear