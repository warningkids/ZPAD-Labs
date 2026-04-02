import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Налаштовуємо сторінку: робимо її широкою (layout="wide") та задаємо назву вкладки у браузері
st.set_page_config(layout="wide", page_title="NOAA Analysis")
# Виводимо головний заголовок на сторінці додатку
st.title("📊 Аналіз індексів VCI / TCI / VHI")

# Створюємо словник для співставлення числових ID з реальними назвами українських областей
REGIONS_DICT = {
    1: 'Вінницька', 2: 'Волинська', 3: 'Дніпропетровська', 4: 'Донецька', 5: 'Житомирська',
    6: 'Закарпатська', 7: 'Запорізька', 8: 'Івано-Франківська', 9: 'Київська', 10: 'Кіровоградська',
    11: 'Луганська', 12: 'Львівська', 13: 'Миколаївська', 14: 'Одеська', 15: 'Полтавська',
    16: 'Рівненська', 17: 'Сумська', 18: 'Тернопільська', 19: 'Харківська', 20: 'Херсонська',
    21: 'Хмельницька', 22: 'Черкаська', 23: 'Чернівецька', 24: 'Чернігівська', 25: 'Республіка Крим',
    26: 'м. Київ', 27: 'м. Севастополь'
}

# Декоратор, який кешує результати функції. Це означає, що при зміні фільтрів дані не будуть читатися з файлів заново
@st.cache_data
def load_data():
    # Задаємо назву папки, де лежать наші файли даних
    folder = "data"
    # Створюємо порожній список для зберігання оброблених таблиць кожної області
    all_data = []

    # Перевіряємо, чи існує папка data
    if not os.path.exists(folder):
        # Якщо ні, виводимо помилку в інтерфейсі
        st.error(f"❌ Папка '{folder}' не знайдена!")
        return None

    # Отримуємо список всіх файлів у папці, які містять "vhi" у назві
    files = [f for f in os.listdir(folder) if "vhi" in f.lower()]
    
    # Якщо таких файлів немає, повертаємо None
    if not files:
        return None

    # Проходимося циклом по кожному знайденому файлу
    for file in files:
        # Формуємо повний шлях до файлу (наприклад, "data/vhi_id_01.csv")
        path = os.path.join(folder, file)
        try:
            # Створюємо список для збереження очищених рядків
            cleaned_lines = []
            # Відкриваємо файл на читання, ігноруючи символи, що не розпізнаються
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                # Читаємо файл рядок за рядком
                for line in f:
                    # Видаляємо зайві HTML-теги, які залишилися після завантаження з сайту
                    line = line.replace('<tt><pre>', '').replace('</pre></tt>', '').replace('<br>', '')
                    # Видаляємо пробіли та коми на початку і в кінці рядка
                    line = line.strip().strip(',')
                    # Якщо рядок не порожній і починається з цифри (тобто це дані, а не заголовок)
                    if line and line[0].isdigit():
                        # Розбиваємо рядок по комах і додаємо отриманий список до cleaned_lines
                        cleaned_lines.append(line.split(','))
            
            # Якщо після очищення даних не лишилося, переходимо до наступного файлу
            if not cleaned_lines:
                continue
                
            # Створюємо DataFrame з очищених даних і задаємо назви колонок
            temp_df = pd.DataFrame(cleaned_lines, columns=['year', 'week', 'smn', 'smt', 'vci', 'tci', 'vhi'])
            # Перетворюємо всі колонки у числовий формат (помилки перетворюються на NaN)
            for col in temp_df.columns:
                temp_df[col] = pd.to_numeric(temp_df[col], errors='coerce')

            # Витягуємо ID області з назви файлу (другий елемент після розбиття по "_")
            region_id = int(file.split('_')[1])
            # Отримуємо красиву назву області зі словника (якщо ID немає, пишемо "Область X")
            region_name = REGIONS_DICT.get(region_id, f"Область {region_id}")
            # Додаємо колонку з назвою області у таблицю
            temp_df["region"] = region_name
            # Додаємо колонку з ID області (знадобиться для правильного сортування)
            temp_df["region_id"] = region_id 

            # Відкидаємо рядки, де VHI дорівнює -1.0 (що означає відсутність даних)
            temp_df = temp_df[temp_df['vhi'] != -1.0]
            # Видаляємо рядки з порожніми значеннями (NaN) і додаємо таблицю до загального списку
            all_data.append(temp_df.dropna())
        # Якщо під час обробки файлу сталась помилка, просто ігноруємо його
        except Exception as e:
            continue

    # Якщо жоден файл не вдалося нормально обробити, повертаємо None
    if not all_data:
        return None

    # Об'єднуємо всі маленькі таблиці з областей в одну велику таблицю
    return pd.concat(all_data, ignore_index=True)

# Запускаємо функцію завантаження даних
df = load_data()

# Якщо дані не завантажились або таблиця порожня
if df is None or df.empty:
    # Виводимо попередження
    st.warning("⚪ Дані не завантажено. Перевірте вміст папки 'data'.")
    # Зупиняємо подальше виконання додатку
    st.stop()

#ФУНКЦІЯ СКИДАННЯ ФІЛЬТРІВ
def reset_filters():
    # Записуємо стандартні (дефолтні) значення в st.session_state (пам'ять сесії Streamlit)
    st.session_state.idx = "vci" # Стандартний індекс
    st.session_state.reg = "Вінницька" # Стандартна область
    st.session_state.weeks = (1, 52) # Весь діапазон тижнів
    st.session_state.years = (int(df['year'].min()), int(df['year'].max())) # Весь діапазон років
    st.session_state.asc = False # Вимикаємо сортування за зростанням
    st.session_state.desc = False # Вимикаємо сортування за спаданням

#ІНТЕРФЕЙС (SIDEBAR)
# Додаємо заголовок на бічну панель
st.sidebar.header("⚙️ Фільтри")

# Створюємо кнопку для скидання фільтрів; при натисканні виконується функція reset_filters (Вимога №5)
st.sidebar.button("🔄 Скинути фільтри", on_click=reset_filters)

# Випадаючий список для вибору індексу (ключ "idx" зв'язує його зі станом сесії)
index_type = st.sidebar.selectbox("Оберіть індекс", ["vci", "tci", "vhi"], key="idx")

# Отримуємо унікальні назви областей разом з їхніми ID та сортуємо їх по ID, щоб вони йшли по порядку (1, 2, 3...)
unique_regions = df[['region', 'region_id']].drop_duplicates().sort_values('region_id')
# Випадаючий список для вибору області (показуємо лише назви)
region = st.sidebar.selectbox("Оберіть область", unique_regions['region'], key="reg")

# Повзунок (слайдер) для вибору інтервалу тижнів (від 1 до 52)
week_range = st.sidebar.slider("Тижні", 1, 52, (1, 52), key="weeks")
# Повзунок для вибору інтервалу років (мінімальний і максимальний роки беремо з самої бази даних)
year_range = st.sidebar.slider("Роки", int(df['year'].min()), int(df['year'].max()), 
                               (int(df['year'].min()), int(df['year'].max())), key="years")

# Малюємо горизонтальну лінію-розділювач на бічній панелі
st.sidebar.markdown("---")
# Додаємо текстовий напис
st.sidebar.write("Сортування таблиці:")
# Створюємо чекбокс для сортування за зростанням (Вимога №9)
sort_asc = st.sidebar.checkbox("За зростанням 📈", key="asc")
# Створюємо чекбокс для сортування за спаданням (Вимога №9)
sort_desc = st.sidebar.checkbox("За спаданням 📉", key="desc")

# === ФІЛЬТРАЦІЯ ДАНИХ ===
# Фільтруємо велику таблицю df за обраними користувачем значеннями (область, діапазон тижнів, діапазон років)
filtered = df[
    (df["region"] == region) &
    (df["week"] >= week_range[0]) & (df["week"] <= week_range[1]) &
    (df["year"] >= year_range[0]) & (df["year"] <= year_range[1])
].copy() # Робимо копію відфільтрованої частини, щоб уникнути помилок при зміні даних

# Логіка сортування та обробка колізії (Вимога №9)
if sort_asc and sort_desc:
    # Якщо користувач увімкнув обидва чекбокси, показуємо попередження
    st.sidebar.warning("⚠️ Обрано обидва сортування! Дані відображено хронологічно.")
    # І сортуємо просто хронологічно: спочатку рік, потім тиждень
    filtered = filtered.sort_values(['year', 'week'])
elif sort_asc:
    # Якщо увімкнено "За зростанням" - сортуємо обраний індекс від найменшого до найбільшого
    filtered = filtered.sort_values(by=index_type, ascending=True)
elif sort_desc:
    # Якщо увімкнено "За спаданням" - сортуємо обраний індекс від найбільшого до найменшого
    filtered = filtered.sort_values(by=index_type, ascending=False)
else:
    # Якщо нічого не обрано - сортуємо хронологічно за замовчуванням
    filtered = filtered.sort_values(['year', 'week'])

#ВКЛАДКИ
# Створюємо 3 вкладки в основній частині сторінки
tab1, tab2, tab3 = st.tabs(["📋 Таблиця", "📈 Графік", "🌍 Порівняння"])

# Відкриваємо першу вкладку
with tab1:
    # Виводимо відфільтрований DataFrame, показуючи лише потрібні колонки. Розтягуємо на всю ширину.
    st.dataframe(filtered[['year', 'week', 'smn', 'smt', 'vci', 'tci', 'vhi', 'region']], use_container_width=True)

# Відкриваємо другу вкладку
with tab2:
    # Перевіряємо, чи є взагалі дані після фільтрації, щоб не будувати порожній графік
    if not filtered.empty:
        # Створюємо об'єкти графіка matplotlib з розміром 10 на 5
        fig, ax = plt.subplots(figsize=(10, 5))
        # Для побудови графіка завжди сортуємо дані по часу, щоб лінія йшла зліва направо і не ламалася
        plot_df = filtered.sort_values(['year', 'week'])
        # Формуємо підписи для осі X у вигляді "Рік-wТиждень" (напр., "2020-w15")
        x_labels = plot_df['year'].astype(str) + "-w" + plot_df['week'].astype(str)
        # Будуємо лінійний графік: по осі X - наші мітки часу, по осі Y - значення обраного індексу
        ax.plot(x_labels, plot_df[index_type], color='tab:blue')
        # Повертаємо мітки на осі X на 90 градусів, щоб вони читались вертикально і не налізали одна на одну
        plt.xticks(rotation=90)
        # Проходимо циклом по всіх мітках осі X
        for i, t in enumerate(ax.get_xticklabels()):
            # Сховуємо 19 з 20 міток (залишаємо кожну 20-ту), щоб не захаращувати вісь підписами
            if i % 20 != 0: t.set_visible(False)
        # Додаємо заголовок графіка
        ax.set_title(f"Динаміка {index_type.upper()} ({region})")
        # Виводимо готовий графік у Streamlit
        st.pyplot(fig)

# Відкриваємо третю вкладку
with tab3:
    # Додаємо підзаголовок
    st.subheader(f"Середнє значення {index_type.upper()} по областях")
    
    # Створюємо нову таблицю для порівняння: фільтруємо ВСІ дані за обраними роками та тижнями
    comp_df = df[
    (df["year"] >= year_range[0]) & (df["year"] <= year_range[1]) &
    (df["week"] >= week_range[0]) & (df["week"] <= week_range[1])
    # Групуємо дані за областями і рахуємо середнє значення (.mean()) для обраного індексу
    ].groupby(["region", "region_id"])[index_type].mean().reset_index()
    
    # Сортуємо результати по ID області, щоб на графіку стовпчики йшли у правильному порядку (1-27)
    comp_df = comp_df.sort_values('region_id')
    
    # Створюємо об'єкти для стовпчастої діаграми
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Задаємо кольори для стовпчиків: помаранчевий для тієї області, яка обрана у фільтрі зліва, блакитний - для всіх інших
    colors = ['tab:orange' if r == region else 'skyblue' for r in comp_df["region"]]
    # Будуємо стовпчасту діаграму (bar chart)
    ax.bar(comp_df["region"], comp_df[index_type], color=colors)
    
    # Повертаємо назви областей на осі X вертикально
    plt.xticks(rotation=90)
    # Підписуємо вісь Y
    ax.set_ylabel(f"Середній {index_type.upper()}")
    # Виводимо графік у Streamlit
    st.pyplot(fig)