import sqlite3
from datetime import datetime

# Файл бази даних
DB_FILE = "database_HabitTracker.db"

# Функція, яка створює або підключається до існуючої бази даних
async def startup():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY,
                 trackers TEXT,
                 language TEXT)''')

    conn.commit()
    conn.close()


# Функція, яка реєструє користувача в базі даних
async def register(user_id, lang_code=None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    language = lang_code if lang_code in ("ru", "uk", "en") else "en"

    c.execute("INSERT OR IGNORE INTO users (id, trackers, language) VALUES (?, ?, ?)",
              (user_id, "[]", language))

    conn.commit()
    conn.close()


# Функція, яка видаляє користувача з бази даних
async def unlogin(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()

# Функція, яка додає трекер користувачу
async def add_tracker(user_id, tracker_name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    now = datetime.now()

    c.execute("SELECT trackers FROM users WHERE id=?", (user_id,))
    trackers_json = c.fetchone()[0]
    trackers_list = eval(trackers_json)
    trackers_list.append({"name": tracker_name, "marks": [], "start": now.strftime("%Y-%m-%d")})
    new_trackers_json = str(trackers_list)

    c.execute("UPDATE users SET trackers=? WHERE id=?", (new_trackers_json, user_id))

    conn.commit()
    conn.close()

# Функція, яка додає відмітку до дати
async def mark_day(user_id, year, month, day, tracker_name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("SELECT trackers FROM users WHERE id=?", (user_id,))
    trackers_json = c.fetchone()[0]
    trackers_list = eval(trackers_json)
    for tracker in trackers_list:
        if tracker["name"] == tracker_name:
            tracker["marks"].append({"year": year, "month": month, "day": day})
            break
    new_trackers_json = str(trackers_list)

    c.execute("UPDATE users SET trackers=? WHERE id=?", (new_trackers_json, user_id))

    conn.commit()
    conn.close()

# Функція, яка прибирає відмітку з дати
async def unmark_day(user_id, year, month, day, tracker_name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("SELECT trackers FROM users WHERE id=?", (user_id,))
    trackers_json = c.fetchone()[0]
    trackers_list = eval(trackers_json)
    for tracker in trackers_list:
        if tracker["name"] == tracker_name:
            tracker["marks"] = [mark for mark in tracker["marks"] if
                                not (mark["year"] == year and mark["month"] == month and mark["day"] == day)]
            break
    new_trackers_json = str(trackers_list)

    c.execute("UPDATE users SET trackers=? WHERE id=?", (new_trackers_json, user_id))

    conn.commit()
    conn.close()

# Функція, яка допомагає визначити, чи позначена дата
def is_marked(user_id, year, month, day, tracker_name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("SELECT trackers FROM users WHERE id=?", (user_id,))
    trackers_json = c.fetchone()[0]
    trackers_list = eval(trackers_json)

    for tracker in trackers_list:
        if tracker["name"] == tracker_name:
            marks_list = tracker.get("marks", [])
            for mark in marks_list:
                if mark.get("year") == year and mark.get("month") == month and mark.get("day") == day:
                    conn.close()
                    return True

    conn.close()
    return False

# Функція, яка повертає список назв трекерів конкретного користувача
async def get_trackers(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("SELECT trackers FROM users WHERE id=?", (user_id,))
    trackers_json = c.fetchone()[0]
    trackers_list = eval(trackers_json)

    tracker_names = [tracker["name"] for tracker in trackers_list]

    conn.close()
    return tracker_names

# Функція, яка видаляє трекер
async def remove_tracker(user_id, tracker_name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("SELECT trackers FROM users WHERE id=?", (user_id,))
    trackers_json = c.fetchone()[0]
    trackers_list = eval(trackers_json)

    updated_trackers_list = [tracker for tracker in trackers_list if tracker["name"] != tracker_name]
    new_trackers_json = str(updated_trackers_list)

    c.execute("UPDATE users SET trackers=? WHERE id=?", (new_trackers_json, user_id))

    conn.commit()
    conn.close()

# Функція, яка перевіряє, чи існує користувач у базі даних
async def check_user_exists(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM users WHERE id=?", (user_id,))
    count = c.fetchone()[0]

    conn.close()
    return count > 0

# Функція, яка перевіряє, чи є дата стартовою для трекера
def is_start_date(user_id, year, month, day, tracker_name):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("SELECT trackers FROM users WHERE id=?", (user_id,))
    trackers_json = c.fetchone()[0]
    trackers_list = eval(trackers_json)

    for tracker in trackers_list:
        if tracker["name"] == tracker_name:
            start_date = datetime.strptime(tracker["start"], "%Y-%m-%d")
            if start_date.year == year and start_date.month == month and start_date.day == day:
                conn.close()
                return True

    conn.close()
    return False

# Функція, яка перейменовує трекер
async def rename_tracker(user_id, tracker_name, tracker_name_new):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("SELECT trackers FROM users WHERE id=?", (user_id,))
    trackers_json = c.fetchone()[0]
    trackers_list = eval(trackers_json)

    for tracker in trackers_list:
        if tracker["name"] == tracker_name:
            tracker["name"] = tracker_name_new
            break

    new_trackers_json = str(trackers_list)

    c.execute("UPDATE users SET trackers=? WHERE id=?", (new_trackers_json, user_id))

    conn.commit()
    conn.close()

async def get_user_lang(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT language FROM users WHERE id=?", (user_id,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else 'en'

async def set_user_lang(user_id, lang_code):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE users SET language=? WHERE id=?", (lang_code, user_id))
    conn.commit()
    conn.close()
