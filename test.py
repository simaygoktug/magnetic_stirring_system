import time
import tkinter as tk  # Tkinter kullanıcı arayüzü için
import random  # Sensör verilerini simüle etmek için

# Motor kontrol fonksiyonu: Motorun hızını simüle ederek ekrana yazdırıyoruz
def control_motor(motor_id, speed):
    print(f"Motor {motor_id}: {speed} RPM hızında çalışıyor")

# Sıcaklık sensöründen veri okuma fonksiyonu (simüle)
def read_temperature():
    # 20°C ile 40°C arasında bir sıcaklık değeri simüle ediyoruz
    return random.uniform(20.0, 40.0)

# pH sensöründen veri okuma fonksiyonu (simüle)
def read_ph():
    # 5.0 ile 9.0 arasında bir pH değeri simüle ediyoruz
    return random.uniform(5.0, 9.0)

# Enkoder geri bildirimi (simüle)
def read_encoder(motor_id):
    # 0 ile 1000 arasında rastgele bir hız değeri simüle ediyoruz
    return random.randint(0, 1000)

# PID kontrol fonksiyonu
def pid_control(setpoint, current_value, integral, previous_error, Kp, Ki, Kd):
    error = setpoint - current_value
    integral += error
    derivative = error - previous_error
    output = Kp * error + Ki * integral + Kd * derivative
    previous_error = error
    return output, integral, previous_error

# Her bölüm için kontrol döngüsü (görevlerle birlikte)
# Optimize edilmiş Kp, Ki, Kd değerleriyle çalışıyor
def control_section(motor_id, tasks, Kp=5.3783, Ki=0.8259, Kd=50.0000):
    for task in tasks:
        if not task:
            continue

        rpm = task['rpm']
        target_time = task['time']
        temp_target = task['temp_target']
        ph_target = task['ph_target']

        start_time = time.time()
        integral_temp, previous_error_temp = 0, 0
        integral_ph, previous_error_ph = 0, 0

        print(f"Motor {motor_id} için görev başlatılıyor - RPM: {rpm}, Sıcaklık Hedefi: {temp_target}, pH Hedefi: {ph_target}, Süre: {target_time}")

        while time.time() - start_time < target_time:
            # Sensörlerden veri simüle ediyoruz
            current_temp = read_temperature()
            current_ph = read_ph()
            current_speed = read_encoder(motor_id)

            print(f"Bölüm {motor_id} - Anlık Sıcaklık: {current_temp:.2f}°C, Anlık pH: {current_ph:.2f}, Hız: {current_speed} RPM")

            # Sıcaklık PID kontrolü
            if temp_target:
                temp_output, integral_temp, previous_error_temp = pid_control(
                    temp_target, current_temp, integral_temp, previous_error_temp, Kp, Ki, Kd)
                print(f"Motor {motor_id} için Sıcaklık PID Çıkışı: {temp_output}")
                control_motor(motor_id, temp_output)

            # pH PID kontrolü
            if ph_target:
                ph_output, integral_ph, previous_error_ph = pid_control(
                    ph_target, current_ph, integral_ph, previous_error_ph, Kp, Ki, Kd)
                print(f"Motor {motor_id} için pH PID Çıkışı: {ph_output}")
                control_motor(motor_id, ph_output)

            # Hız PID kontrolü (Geri bildirim ekleme)
            speed_output, _, _ = pid_control(rpm, current_speed, 0, 0, Kp, Ki, Kd)
            control_motor(motor_id, speed_output)

            time.sleep(1)

        print(f"Bölüm {motor_id}, {target_time} saniye sonra görevi tamamladı.")

# Kullanıcı arayüzü: Parametrelerin ayarlanması ve her bölüm için 3 adımlı görevlerin desteklenmesi
def setup_interface():
    root = tk.Tk()
    root.title("Simüle Edilmiş Manyetik Karıştırıcı Kontrol")
    root.configure(bg="#F7F7F7")  # Açık renkli arka plan

    # Pencereyi ekranda ortalıyoruz
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

    # İçeriklerin ortalanması için bir çerçeve oluşturuyoruz
    frame = tk.Frame(root, bg="#F7F7F7", padx=20, pady=20)
    frame.pack(expand=True)

    # Her bölüm için görevleri ayarlayan ve başlatan fonksiyonu oluşturuyoruz
    def set_section_params(section):
        tasks = []
        for i in range(3):  # Her bölüm için en fazla 3 görev
            rpm = int(rpm_vars[section-1][i].get()) if rpm_vars[section-1][i].get() else 0
            time_period = int(time_vars[section-1][i].get()) if time_vars[section-1][i].get() else 0
            temp_target = float(temp_vars[section-1][i].get()) if temp_vars[section-1][i].get() else None
            ph_target = float(ph_vars[section-1][i].get()) if ph_vars[section-1][i].get() else None

            task = {'rpm': rpm, 'time': time_period, 'temp_target': temp_target, 'ph_target': ph_target}
            tasks.append(task)

        print(f"Bölüm {section} başlatılıyor, görevler: {tasks}")

        # Bölümü çalıştırıyoruz
        control_section(section, tasks)

    # Her bölüm ve görev için etiketler ve giriş alanları oluşturuyoruz
    rpm_vars = [[] for _ in range(6)]
    time_vars = [[] for _ in range(6)]
    temp_vars = [[] for _ in range(6)]
    ph_vars = [[] for _ in range(6)]

    for section in range(1, 7):
        tk.Label(frame, text=f"Bölüm {section}", bg="#F7F7F7", font=("Arial", 12, "bold")).grid(row=section*4-3, column=0, pady=10)

        for task in range(3):  # Her bölüm için 3 görev
            tk.Label(frame, text=f"Görev {task+1} - RPM", bg="#F7F7F7").grid(row=section*4-2+task, column=1)
            rpm_var = tk.StringVar()
            tk.Entry(frame, textvariable=rpm_var, width=10).grid(row=section*4-2+task, column=2)
            rpm_vars[section-1].append(rpm_var)

            tk.Label(frame, text="Süre (s)", bg="#F7F7F7").grid(row=section*4-2+task, column=3)
            time_var = tk.StringVar()
            tk.Entry(frame, textvariable=time_var, width=10).grid(row=section*4-2+task, column=4)
            time_vars[section-1].append(time_var)

            tk.Label(frame, text="Sıcaklık (°C)", bg="#F7F7F7").grid(row=section*4-2+task, column=5)
            temp_var = tk.StringVar()
            tk.Entry(frame, textvariable=temp_var, width=10).grid(row=section*4-2+task, column=6)
            temp_vars[section-1].append(temp_var)

            tk.Label(frame, text="pH", bg="#F7F7F7").grid(row=section*4-2+task, column=7)
            ph_var = tk.StringVar()
            tk.Entry(frame, textvariable=ph_var, width=10).grid(row=section*4-2+task, column=8)
            ph_vars[section-1].append(ph_var)

        # Görevleri başlatma butonu
        tk.Button(frame, text="Bölümü Başlat", command=lambda s=section: set_section_params(s), bg="#4CAF50", fg="white", width=12).grid(row=section*4-2, column=9, rowspan=3, padx=10, pady=5)

    root.mainloop()

if __name__ == "__main__":
    setup_interface()
