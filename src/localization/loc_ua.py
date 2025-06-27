HELP_COMMAND = """
<b>/start</b> - <em>Запустити бота</em>
<b>/help</b> - <em>Інформація про команди</em>
<b>/menu</b> - <em>Головне меню трекерів</em>
<b>/unlogin</b> - <em>Видалити себе з бази даних</em>
<b>/language</b> - <em>Змінити мову</em>
"""

START = """
Ласкаво просимо до бота!
Цей бот призначений для створення трекерів звичок!
Щоб розпочати — скористайтесь командою /menu
Щоб переглянути список команд — /help
"""

H_UNLOGIN_TRUE = "Ви впевнені, що хочете видалити всі свої записи?"

H_UNLOGIN_FALSE = "У вас ще немає жодного запису!\nЩоб створити — просто відкрийте меню: /menu"

H_MENU = "Меню ваших трекерів, оберіть опцію!"

H_NEW = "Введіть назву для вашого трекера:"

H_CHOISE_TRUE = "Оберіть трекер!"

H_CHOISE_FALSE = "У вас ще немає трекерів :(\nПерейдіть до меню, щоб створити новий!"

H_TRACKER_MENU = "Оберіть опцію"

H_TRACKER_RENAME_TRUE = "Оберіть трекер для перейменування"

H_TRACKER_RENAME_FALSE = "У вас ще немає трекерів :(\nПерейдіть до меню, щоб створити новий!"

H_PROFILE_DELETED = "Вас більше немає в базі даних!"

H_TRACKER_DELETE_TRUE = "Оберіть трекер для видалення"

H_TRACKER_DELETE_FALSE = "У вас більше не залишилося трекерів :(\nПерейдіть до меню, щоб створити новий!"


def tracker_delete_confirm(tracker=""):
    return f"Ви впевнені, що хочете видалити трекер '{tracker}'?"


H_TRACKER_RENAME = "Введіть нову назву:"


def tracker_output(tracker=""):
    return f"Трекер '{tracker}'"


H_TRACKER_CREATE_TRUE = "Схоже, у вас вже є такий трекер... Введіть іншу назву!"


def tracker_false(tracker=""):
    return f"Готово! Ваш трекер '{tracker}' готовий до використання!"


H_STATE_DECLINE = "Дію скасовано, спробуйте ще раз!"

B_MAIN_YOUR_TRACKERS = "Ваші трекери"

B_MAIN_MENU_TRACKERS = "Меню трекерів"

B_MAIN_CREATE_TRACKER = "Створити новий трекер"

B_CLOSE = "Закрити"

B_TRACKER_DELETE = "Видалити трекер"

B_TRACKER_RENAME = "Змінити назву"

B_BACK = "Назад"

B_YES = "Так"

B_NO = "Ні"

LOC = "uk_UA.UTF-8"

H_LOC_ANSWER = "Мову змінено ✅"

B_LOC_ENG = "Англійська"
B_LOC_UA = "Українська"
B_LOC_RU = "Російська"

H_LOC_MENU = "Оберіть мову:"