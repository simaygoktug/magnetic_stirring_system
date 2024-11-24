% pid_performance.m

function perf = pid_performance(x, motor_tf)
    Kp = x(1); Ki = x(2); Kd = x(3);
    pid_controller = pid(Kp, Ki, Kd);  % PID denetleyiciyi oluştur
    closed_loop_tf = feedback(series(pid_controller, motor_tf), 1);  % Kapalı çevrim transfer fonksiyonu

    % Adım yanıtı verilerini al
    [y, t] = step(closed_loop_tf);

    % Performans metriklerini hesapla
    info = stepinfo(closed_loop_tf);
    
    % Performans indeksi tanımla: yerleşme süresi, aşım ve yükselme süresinin kombinasyonu
    perf = info.SettlingTime + info.Overshoot + info.RiseTime;
    
    % Fazla aşım veya yavaş yanıt için ceza ekle
    if info.Overshoot > 20  % Aşım %20'den fazla ise cezalandır
        perf = perf + 1000;
    end
    
    % Yerleşme süresi belirli bir sınırı geçerse ceza ekle
    if info.SettlingTime > 5  % Örneğin 5 saniye üzerindeki yerleşme süreleri için ceza
        perf = perf + 500;
    end
    
    % Ekstra: Kararlılık metriği (osilasyonları cezalandırmak için)
    if any(y > 1.1 | y < 0.9)  % %10'un üzerinde aşırı sapmalar varsa ceza 
        perf = perf + 1500;
    end
end
