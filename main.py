import RPi.GPIO as GPIO
import time
import Adafruit_DHT
import tkinter as tk

# Motorlar ve enkoder için pinleri tanımlıyoruz
MOTOR_PINS = {
    1: {'IN1': 17, 'IN2': 18, 'ENA': 22, 'ENC_A': 27, 'ENC_B': 22},  # 1. Motor ve enkoder pinleri
    2: {'IN1': 23, 'IN2': 24, 'ENA': 25, 'ENC_A': 19, 'ENC_B': 26},  # 2. Motor ve enkoder pinleri
    3: {'IN1': 27, 'IN2': 17, 'ENA': 4, 'ENC_A': 21, 'ENC_B': 20},   # 3. Motor ve enkoder pinleri
    4: {'IN1': 5, 'IN2': 6, 'ENA': 13, 'ENC_A': 14, 'ENC_B': 15},    # 4. Motor ve enkoder pinleri
    5: {'IN1': 19, 'IN2': 26, 'ENA': 20, 'ENC_A': 10, 'ENC_B': 9},   # 5. Motor ve enkoder pinleri
    6: {'IN1': 21, 'IN2': 22, 'ENA': 16, 'ENC_A': 11, 'ENC_B': 8}    # 6. Motor ve enkoder pinleri
}

# Sensörler için pinleri tanımlıyoruz
TEMP_PIN = 4  # Sıcaklık sensörü için GPIO pini (DS18B20 veya DHT22)
PH_PIN = 0    # pH sensörü için pin (Atlas Scientific veya ADC ile MCP3008)

# Optimize edilmiş PID kontrol parametrelerini tanımlıyoruz
Kp = 0.3000
Ki = 0.0030
Kd = 35.0300

# Kullanıcı tarafından ayarlanan değerleri her bölüm için tanımlıyoruz (6 motor)
user_settings = {
    1: {'tasks': []},
    2: {'tasks': []},
    3: {'tasks': []},
    4: {'tasks': []},
    5: {'tasks': []},
    6: {'tasks': []}
}

# Enkoder geri bildirimi için hız değişkenlerini tanımlıyoruz
motor_speed = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
previous_ticks = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

# GPIO ayarlarını yapıyoruz
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Motorları kuruyoruz
for motor, pins in MOTOR_PINS.items():
    GPIO.setup(pins['IN1'], GPIO.OUT)
    GPIO.setup(pins['IN2'], GPIO.OUT)
    GPIO.setup(pins['ENA'], GPIO.OUT)
    GPIO.setup(pins['ENC_A'], GPIO.IN)  # Enkoder A pini
    GPIO.setup(pins['ENC_B'], GPIO.IN)  # Enkoder B pini
    pins['pwm'] = GPIO.PWM(pins['ENA'], 100)  # PWM frekansını 100Hz olarak ayarlıyoruz
    pins['pwm'].start(0)  # PWM başlangıçta 0 görev döngüsü ile başlıyor

# DHT22 sıcaklık sensörünü başlatıyoruz
DHT_SENSOR = Adafruit_DHT.DHT22

# Sıcaklık sensöründen veri okuyoruz
def read_temperature():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, TEMP_PIN)
    if temperature:
        return temperature
    return None

# pH sensöründen veri okuyoruz (Atlas Scientific)
def read_ph():
    return 7.0  # Örnek pH değeri

# Enkoder geri bildiriminden hız okuma
def read_encoder(motor_id):
    global motor_speed, previous_ticks
    pins = MOTOR_PINS[motor_id]
    ticks = GPIO.input(pins['ENC_A'])  # Enkoder A kanalından veri okuyoruz
    # Burada hız hesaplamak için eklenmesi gereken mantık
    if ticks != previous_ticks[motor_id]:
        motor_speed[motor_id] += 1 if ticks else -1
        previous_ticks[motor_id] = ticks
    return motor_speed[motor_id]

# PID kontrol fonksiyonunu oluşturuyoruz
def pid_control(setpoint, current_value, integral, previous_error):
    error = setpoint - current_value
    integral += error
    derivative = error - previous_error
    output = Kp * error + Ki * integral + Kd * derivative
    previous_error = error
    return output, integral, previous_error

# Motor kontrol fonksiyonu
def control_motor(motor_id, speed):
    pins = MOTOR_PINS[motor_id]
    if speed > 0:
        GPIO.output(pins['IN1'], GPIO.HIGH)
        GPIO.output(pins['IN2'], GPIO.LOW)
    elif speed < 0:
        GPIO.output(pins['IN1'], GPIO.LOW)
        GPIO.output(pins['IN2'], GPIO.HIGH)
    else:
        GPIO.output(pins['IN1'], GPIO.LOW)
        GPIO.output(pins['IN2'], GPIO.LOW)
    
    pwm_speed = max(0, min(100, abs(speed)))
    pins['pwm'].ChangeDutyCycle(pwm_speed)

# Her motor için görevleri kontrol eden ana fonksiyon
def control_section(motor_id, tasks):
    for task in tasks:
        rpm = task['rpm']
        target_time = task['time']
        temp_target = task['temp_target']
        ph_target = task['ph_target']

        start_time = time.time()
        integral_temp, previous_error_temp = 0, 0
        integral_ph, previous_error_ph = 0, 0

        while time.time() - start_time < target_time:
            current_temp = read_temperature()
            current_ph = read_ph()
            current_speed = read_encoder(motor_id)

            if temp_target and current_temp:
                temp_output, integral_temp, previous_error_temp = pid_control(
                    temp_target, current_temp, integral_temp, previous_error_temp)
                control_motor(motor_id, temp_output)

            if ph_target and current_ph:
                ph_output, integral_ph, previous_error_ph = pid_control(
                    ph_target, current_ph, integral_ph, previous_error_ph)
                control_motor(motor_id, ph_output)

            if not temp_target and not ph_target:
                control_motor(motor_id, rpm)

            time.sleep(1)

# Kullanıcı arayüzü
def setup_interface():
    root = tk.Tk()
    root.title("Manyetik Karıştırıcı Kontrol Paneli")
    root.configure(bg="#F7F7F7")

    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

    frame = tk.Frame(root, bg="#F7F7F7", padx=20, pady=20)
    frame.pack(expand=True)

    # Bölüm parametrelerini ayarlayan fonksiyonları burada tekrar ekliyoruz
    root.mainloop()

if __name__ == "__main__":
    setup_interface()
