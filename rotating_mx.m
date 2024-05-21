

alpha = pi;
nu = -pi/2;
a = 0;
d = 0;

Ry = [cos(alpha) 0 sin(alpha);
           0      0      0;
      -sin(alpha) 0 cos(alpha)];

Rz = [cos(nu) -sin(nu) 0;
      sin(nu) cos(nu)  0;
           0           0       0];

R = Rz * Ry;
r = [140 -40 0];

Rotated = r * R;

T = [cos(nu) -sin(nu) 0 a;
    cos(alpha)*sin(nu) cos(alpha)*cos(nu) -sin(alpha) -d*sin(alpha);
    sin(alpha)*sin(nu) sin(alpha)*cos(nu) cos(alpha) d*cos(alpha);
    0 0 0 1]; 

r = [170 -180 0 1];

Trotated = r * T