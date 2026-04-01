import numpy as np
# Імпорт модуля pyplot з Matplotlib для створення вікон та малювання графіків
import matplotlib.pyplot as plt
# Імпорт інтерактивних віджетів (слайдери, кнопки, чекбокси) з Matplotlib
from matplotlib.widgets import Slider, Button, CheckButtons
# Імпорт функцій для створення (butter) та застосування (filtfilt) цифрового фільтра
from scipy.signal import butter, filtfilt

#ІНСТРУКЦІЯ ДЛЯ КОРИСТУВАЧА
# Виведення багаторядкового тексту з інструкцією у консоль при запуску програми
print("""
=== ІНСТРУКЦІЯ ===
1. Використовуйте слайдери для зміни параметрів гармоніки (Амплітуда, Частота, Фаза).
2. Використовуйте слайдери параметрів шуму (Середнє, Дисперсія). Шум генерується наново ТІЛЬКИ при зміні цих параметрів.
3. Слайдер 'Зріз фільтра' дозволяє налаштувати частоту пропускання фільтра Баттерворта.
4. Чекбокс 'Показувати шум' вмикає/вимикає накладання шуму на початковий сигнал.
5. Кнопка 'Скинути' повертає всі параметри до початкових значень.
""")

#ЧАС
# Створення масиву з 1000 точок, рівномірно розподілених від 0 до 10 (вісь X)
t = np.linspace(0, 10, 1000)

#ПОЧАТКОВІ ПАРАМЕТРИ
A0 = 1.0 # Початкова амплітуда (A)
f0 = 1.0 # Початкова частота (f)
phi0 = 0.0 # Початковий фазовий зсув (phi)
noise_mean0 = 0.0 # Початкове математичне сподівання (середнє значення) шуму
noise_var0 = 0.2 # Початкова дисперсія (розкид) шуму
show_noise0 = True # Флаг, який визначає, чи показувати шум при запуску (True = показувати)
cutoff0 = 0.1 # Початкова частота зрізу для фільтра Баттерворта

#ГЛОБАЛЬНИЙ ШУМ
# Генерація масиву нормально розподіленого (гауссівського) шуму згідно з початковими параметрами
noise = np.random.normal(noise_mean0, noise_var0, len(t))

#ФУНКЦІЯ
# Функція для генерації гармонійного сигналу (з шумом або без)
def harmonic_with_noise(amplitude, frequency, phase,noise_mean, noise_covariance, show_noise):
    # Обчислення "чистої" гармоніки за формулою y(t) = A * sin(2*pi*f*t + phi) (тут без 2*pi для спрощення)
    clean = amplitude * np.sin(frequency * t + phase)
    # Звернення до глобальної змінної noise, щоб не генерувати шум наново при кожному виклику
    global noise
    # Якщо чекбокс увімкнено, додаємо масив шуму до чистого сигналу
    if show_noise:
        signal = clean + noise
    # Якщо вимкнено, повертаємо просто чистий сигнал
    else:
        signal = clean
    # Функція повертає два масиви: чисту гармоніку та сигнал (з шумом або без)
    return clean, signal

# ФІЛЬТР
# Функція для застосування низькочастотного фільтра Баттерворта
def apply_filter(signal, cutoff):
    # Створення коефіцієнтів (b, a) для фільтра 3-го порядку з заданою частотою зрізу
    # cutoff має бути в межах від 0 до 1 (відносно частоти Найквіста)
    b, a = butter(3, cutoff)
    # Застосування фільтра filtfilt (фільтрація вперед і назад для уникнення фазового зсуву)
    return filtfilt(b, a, signal)

#ГРАФІКИ
fig, (ax1, ax2) = plt.subplots(2, 1) # Створення вікна (fig) та двох графіків (ax1 - верхній, ax2 - нижній)
fig.set_size_inches(10, 8) # Встановлення розміру вікна у дюймах (ширина 10, висота 8)

# Налаштування відступів вікна, щоб звільнити місце знизу для слайдерів
plt.subplots_adjust(left=0.1, bottom=0.45, right=0.95, top=0.95)

# Отримання початкових даних для малювання
clean, signal = harmonic_with_noise(A0, f0, phi0,noise_mean0, noise_var0, show_noise0)
# Фільтрація початкового сигналу
filtered = apply_filter(signal, cutoff0)

# Малювання графіка зашумленого сигналу на верхньому полотні (зберігаємо об'єкт лінії у змінну)
line_signal, = ax1.plot(t, signal, label="Зашумлена гармоніка")
# Малювання графіка чистої гармоніки на верхньому полотні (пунктиром '--')
line_clean, = ax1.plot(t, clean, '--', label="Чиста гармоніка")
# Малювання відфільтрованого сигналу на нижньому полотні (зеленим кольором)
line_filtered, = ax2.plot(t, filtered, label="Відфільтрована гармоніка", color='green')

# Додавання заголовків для кожного з графіків
ax1.set_title("Початковий сигнал")
ax2.set_title("Відфільтрований сигнал")

# Відображення легенди (підписів ліній) на обох графіках
ax1.legend()
ax2.legend()
# Увімкнення сітки для кращої візуалізації
ax1.grid(True)
ax2.grid(True)

#СЛАЙДЕРИ
# Створення спеціальних осей (прямокутників) для розміщення слайдерів: [ліво, низ, ширина, висота]
ax_A = plt.axes([0.1, 0.35, 0.8, 0.03])
ax_f = plt.axes([0.1, 0.31, 0.8, 0.03])
ax_phi = plt.axes([0.1, 0.27, 0.8, 0.03])
ax_noise_mean = plt.axes([0.1, 0.23, 0.8, 0.03])
ax_noise_var = plt.axes([0.1, 0.19, 0.8, 0.03])
ax_cutoff = plt.axes([0.1, 0.15, 0.8, 0.03])

# Створення самих об'єктів слайдерів з вказівкою осей, назви, мін/макс значень та початкового значення
sA = Slider(ax_A, 'Амплітуда', 0.1, 5.0, valinit=A0)
sf = Slider(ax_f, 'Частота', 0.1, 5.0, valinit=f0)
sphi = Slider(ax_phi, 'Фаза', 0, 3.14, valinit=phi0)
s_noise_mean = Slider(ax_noise_mean, 'Сер. шуму', -1.0, 1.0, valinit=noise_mean0)
s_noise_var = Slider(ax_noise_var, 'Дисперсія', 0.01, 1.0, valinit=noise_var0)
# Слайдер для фільтра, макс. значення 0.49 (щоб не доходило до 1.0, що викличе помилку фільтра)
s_cutoff = Slider(ax_cutoff, 'Зріз фільтра', 0.01, 0.49, valinit=cutoff0)

#ЧЕКБОКС
# Створення осей для чекбокса
ax_check = plt.axes([0.1, 0.04, 0.2, 0.04])
# Створення чекбокса 'Показувати шум' зі статусом увімкнено (True)
check = CheckButtons(ax_check, ['Показувати шум'], [True])

#КНОПКА
ax_reset = plt.axes([0.75, 0.02, 0.2, 0.05]) # Створення осей для кнопки 'Скинути'
btn = Button(ax_reset, 'Скинути') # Створення самої кнопки

#СТАН ШУМУ
# Змінні для зберігання попередніх значень параметрів шуму, щоб перевіряти, чи змінювались вони
prev_noise_mean = noise_mean0
prev_noise_var = noise_var0

#ОНОВЛЕННЯ
# Функція, яка викликається при будь-якій зміні повзунків або чекбокса
def update(val):
    # Оголошуємо глобальними змінні шуму та його попередніх станів
    global noise, prev_noise_mean, prev_noise_var

    # Зчитуємо поточні значення з усіх слайдерів
    A = sA.val
    f = sf.val
    phi = sphi.val
    noise_mean = s_noise_mean.val
    noise_var = s_noise_var.val
    cutoff = s_cutoff.val
    # Зчитуємо стан чекбокса (True або False)
    show_noise = check.get_status()[0]

    # Якщо параметри шуму відрізняються від попередніх, генеруємо новий масив шуму
    if noise_mean != prev_noise_mean or noise_var != prev_noise_var:
        noise = np.random.normal(noise_mean, noise_var, len(t))
        # Оновлюємо значення попередніх станів для наступних перевірок
        prev_noise_mean = noise_mean
        prev_noise_var = noise_var

    # Перераховуємо чисту гармоніку та сигнал з шумом з новими параметрами
    clean, signal = harmonic_with_noise(A, f, phi,noise_mean, noise_var, show_noise)

    # Застосовуємо фільтр до оновленого сигналу
    filtered = apply_filter(signal, cutoff)

    # Оновлюємо дані Y для ліній на графіках (без перемальовування всього вікна з нуля)
    line_signal.set_ydata(signal)
    line_clean.set_ydata(clean)
    line_filtered.set_ydata(filtered)

    # Динамічне перемасштабування осей Y (щоб графік не вилізав за краї, якщо збільшити амплітуду)
    ax1.relim()             # Перераховуємо ліміти даних для верхнього графіка
    ax1.autoscale_view()    # Застосовуємо новий масштаб
    ax2.relim()             # Перераховуємо ліміти даних для нижнього графіка
    ax2.autoscale_view()    # Застосовуємо новий масштаб

    # Сигнал для Matplotlib перемалювати вікно графіка (застосувати зміни)
    fig.canvas.draw_idle()

# Прив'язка функції update до події зміни значень на кожному зі слайдерів
sA.on_changed(update)
sf.on_changed(update)
sphi.on_changed(update)
s_noise_mean.on_changed(update)
s_noise_var.on_changed(update)
s_cutoff.on_changed(update)
# Прив'язка функції update до кліку по чекбоксу
check.on_clicked(update)

#RESET
# Функція для скидання всіх параметрів до початкових значень (викликається кнопкою)
def reset(event):
    global noise, prev_noise_mean, prev_noise_var

    # Вимикаємо відстеження подій для слайдерів під час скидання, щоб функція update не викликалась 6 разів поспіль
    events = [sA, sf, sphi, s_noise_mean, s_noise_var, s_cutoff]
    for slider in events:
        slider.eventson = False # Тимчасово відключаємо події
        slider.reset()          # Скидаємо слайдер на початкове значення
        slider.eventson = True  # Вмикаємо події назад

    # Перевіряємо статус чекбокса. Якщо він вимкнений, то вмикаємо його (index 0)
    if not check.get_status()[0]:
        check.set_active(0)

    # Генеруємо початковий шум
    noise = np.random.normal(noise_mean0, noise_var0, len(t))
    # Скидаємо попередні значення параметрів шуму
    prev_noise_mean = noise_mean0
    prev_noise_var = noise_var0

    # Викликаємо оновлення графіків один раз наприкінці
    update(None)

# Прив'язка функції reset до натискання на кнопку "Скинути"
btn.on_clicked(reset)

# Команда для запуску та відображення вікна з графіками та інтерфейсом
plt.show()