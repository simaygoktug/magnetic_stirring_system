% RS-550 Motoru için Ana PID Optimizasyon Scripti

% Mabuchi RS550 motorunun sistem parametreleri
J = 5.9e-6;  % Rotor atalet momenti (kg·m²), datasheet verisi
B = 1.2e-6;  % Sönümleme katsayısı (N·m·s), tahmini
R = 1.2;     % Armatür direnci (Ohm), datasheet verisi
Kt = 0.017;  % Motor tork sabiti (N·m/A), datasheet verisi
Kb = 0.017;  % Geri EMF sabiti (V·s/rad), datasheet verisi

% Encoder parametreleri
encoder_cpr = 12;  % Pololu encoder Cycles per Revolution değeri
wheel_diameter = 0.025;  % Motor bağlı tekerlek çapı (m), datasheet verisi

% DC motorun transfer fonksiyonu
num = Kt;  % Pay (motor tork sabiti)
den = [(J*R) (B*R + J*Kb) (B*Kb + Kt^2)];  % Payda
motor_tf = tf(num, den);

% Kp, Ki, Kd için başlangıç tahminleri
initial_guess = [1, 0.01, 0.1];

% Kp, Ki, Kd için alt ve üst sınırları
lb = [0, 0, 0];  % Alt sınırlar
ub = [100, 10, 50];  % Üst sınırlar

% Optimizasyon seçeneklerini tanımla
options = optimoptions('fmincon', 'Display', 'iter', 'Algorithm', 'sqp', 'MaxIterations', 100);

% fmincon fonksiyonunu çalıştırarak optimal PID parametreleri
optimal_values = fmincon(@(x) pid_performance(x, motor_tf), initial_guess, [], [], [], [], lb, ub, [], options);

% Optimal PID değerleri
Kp_opt = optimal_values(1);
Ki_opt = optimal_values(2);
Kd_opt = optimal_values(3);

% Optimize edilmiş PID değerlerini ekrana yazdır
fprintf('RS-550 Motoru için Optimal PID değerleri:\nKp: %.4f, Ki: %.4f, Kd: %.4f\n', Kp_opt, Ki_opt, Kd_opt);

% Bu değerleri bir dosyaya kaydet
fileID = fopen('optimal_pid_values_rs550.txt', 'w');
fprintf(fileID, 'RS-550 Motoru için Optimal PID değerleri:\nKp: %.4f\nKi: %.4f\nKd: %.4f\n', Kp_opt, Ki_opt, Kd_opt);
fclose(fileID);

% Optimize edilmiş adım yanıtını çiz
optimized_pid = pid(Kp_opt, Ki_opt, Kd_opt);
optimized_open_loop_tf = series(optimized_pid, motor_tf);
optimized_closed_loop_tf = feedback(optimized_open_loop_tf, 1);

% Adım yanıtını analiz edip performans metrikleri
[y, t] = step(optimized_closed_loop_tf);  % Adım yanıtı verilerini al

% Performans metrikleri
info = stepinfo(optimized_closed_loop_tf);  % MATLAB'in adım yanıtı bilgisi fonksiyonunu kullan
rise_time = info.RiseTime;
overshoot = info.Overshoot;
settling_time = info.SettlingTime;
steady_state_error = abs(1 - y(end));  % Adım girişinin genliği 1 olarak varsayılıyor

% Performans metriklerini ekrana yazdır
fprintf('--- RS-550 için PID Denetleyici Performans Metrikleri ---\n');
fprintf('Yükselme Süresi: %.4f saniye\n', rise_time);
fprintf('Aşım: %.2f%%\n', overshoot);
fprintf('Yerleşme Süresi: %.4f saniye\n', settling_time);
fprintf('Kalıcı Durum Hatası: %.4f\n', steady_state_error);

% Performans metriklerini bir dosyaya kaydet
fileID = fopen('pid_performance_metrics_rs550.txt', 'w');
fprintf(fileID, '--- RS-550 için PID Denetleyici Performans Metrikleri ---\n');
fprintf(fileID, 'Yükselme Süresi: %.4f saniye\n', rise_time);
fprintf(fileID, 'Aşım: %.2f%%\n', overshoot);
fprintf(fileID, 'Yerleşme Süresi: %.4f saniye\n', settling_time);
fprintf(fileID, 'Kalıcı Durum Hatası: %.4f\n', steady_state_error);
fclose(fileID);

% Adım yanıtı grafiği
figure;
step(optimized_closed_loop_tf);
title('RS-550 DC Motorunun PID Kontrol ile Optimize Edilmiş Adım Yanıtı');
grid on;