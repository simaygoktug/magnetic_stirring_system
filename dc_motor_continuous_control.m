% Parameters for DC Motor
R = 1.0;   % Armature resistance (Ohms)
L = 0.5;   % Armature inductance (H)
Kb = 0.01; % Back EMF constant (V/rad/s)
Kt = 0.01; % Torque constant (Nm/A)
J = 0.01;  % Rotor inertia (kg*m^2)
b = 0.1;   % Damping coefficient (Nm*s/rad)

% Transfer function of the DC motor
num_motor = Kt;
den_motor = [J*L, (J*R + L*b), (R*b + Kb*Kt)];
motor_tf = tf(num_motor, den_motor);

% PID Controller parameters
Kp = 100;   % Proportional gain
Ki = 200;   % Integral gain
Kd = 10;    % Derivative gain
PID_Controller = pid(Kp, Ki, Kd);

% Closed-loop transfer functions for position and velocity control
closed_loop_pos_sys = feedback(PID_Controller * motor_tf, 1);
closed_loop_vel_sys = feedback(PID_Controller * motor_tf, 1);

% Time vector for simulation
t = 0:0.01:10; % 10 seconds simulation

% 1. Position Reference Control: r(t) = 10 * sin(2 * pi * 1 * t)
position_ref = 10 * sin(2 * pi * 1 * t); % Position reference signal

% Simulate response for position control
[y_pos, t_pos] = lsim(closed_loop_pos_sys, position_ref, t);

% Plot results for position tracking
figure;
plot(t_pos, position_ref, 'r--', 'DisplayName', 'Position Reference');
hold on;
plot(t_pos, y_pos, 'b', 'DisplayName', 'Motor Position');
title('Position Reference Tracking (10*sin(2*pi*1*t))');
xlabel('Time (s)');
ylabel('Position (rad)');
legend;
grid on;

% 2. Velocity Reference Control: r(t) = 30 + 20 * sin(2 * pi * 0.1 * t)
velocity_ref = 30 + 20 * sin(2 * pi * 0.1 * t); % Velocity reference signal

% Simulate response for velocity control
[y_vel, t_vel] = lsim(closed_loop_vel_sys, velocity_ref, t);

% Plot results for velocity tracking
figure;
plot(t_vel, velocity_ref, 'r--', 'DisplayName', 'Velocity Reference');
hold on;
plot(t_vel, y_vel, 'b', 'DisplayName', 'Motor Velocity');
title('Velocity Reference Tracking (30 + 20*sin(2*pi*0.1*t))');
xlabel('Time (s)');
ylabel('Velocity (rad/s)');
legend;
grid on;
