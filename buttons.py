import calendar
import locale
from datetime import datetime
import habitTrackerDataBase as sq
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)
from src.localization.localization import language_setup
from src.callbackdatas import language

# Функція, яка повертає кнопку для виклику меню
def get_start_buttons():
    btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn.row(KeyboardButton('/menu'))
    return btn


# Функція, яка повертає кнопки з головного меню
async def get_menu_buttons(user_id):
    btn = InlineKeyboardMarkup()
    loc = await language_setup(user_id)
    btn.row(InlineKeyboardButton(loc.B_MAIN_YOUR_TRACKERS, callback_data='menu'))
    btn.row(InlineKeyboardButton(loc.B_MAIN_MENU_TRACKERS, callback_data='tracker_menu'),  # tracker_delete_menu
            InlineKeyboardButton(loc.B_MAIN_CREATE_TRACKER, callback_data='new'))
    btn.row(InlineKeyboardButton(loc.B_CLOSE, callback_data='close'))
    return btn


async def get_loc_buttons(user_id):
    btn = InlineKeyboardMarkup()
    loc = await language_setup(user_id)

    btn.row(
        InlineKeyboardButton(loc.B_LOC_ENG, callback_data=language.new("en")),
        InlineKeyboardButton(loc.B_LOC_UA, callback_data=language.new("uk")),
    )
    btn.row(InlineKeyboardButton(loc.B_CLOSE, callback_data='close'))
    return btn


# Функція, яка повертає кнопки меню трекерів
async def get_tracker_menu_buttons(user_id):
    btn = InlineKeyboardMarkup()
    loc = await language_setup(user_id)
    btn.row(InlineKeyboardButton(loc.B_TRACKER_DELETE, callback_data='tracker_delete_menu'),
            InlineKeyboardButton(loc.B_TRACKER_RENAME, callback_data='tracker_rename_menu'))
    btn.row(InlineKeyboardButton(loc.B_BACK, callback_data="back"))
    return btn


# Функція, яка повертає кнопку допомоги
def get_help_buttons():
    btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn.insert(KeyboardButton('/menu'))
    return btn


# Функція, яка повертає кнопки підтвердження видалення трекера
async def get_confirmation_deltrack_button(tracker, user_id):
    btn = InlineKeyboardMarkup()
    loc = await language_setup(user_id)
    btn.row(InlineKeyboardButton(loc.B_YES, callback_data=f'tracker_delete_{tracker}'),
            InlineKeyboardButton(loc.B_BACK, callback_data='tracker_delete_menu'))
    return btn


# Функція, яка повертає кнопки підтвердження видалення профілю
async def get_confirmation_delprofile_button(user_id):
    btn = InlineKeyboardMarkup()
    loc = await language_setup(user_id)
    btn.row(InlineKeyboardButton(loc.B_YES, callback_data=f'profile_delete'),
            InlineKeyboardButton(loc.B_NO, callback_data='profile_delete_decline'))
    return btn


# Функція, яка генерує та повертає кнопки з переданого списку (трекерів)
async def generate_tracker_buttons(names, action, user_id):
    btn = InlineKeyboardMarkup(row_width=3)

    loc = await language_setup(user_id)
    if action == 'choise':
        for name in names:
            btn.insert(InlineKeyboardButton(name, callback_data=f"tracker_{name}"))
        btn.row(InlineKeyboardButton(loc.B_BACK, callback_data="back"))
        return btn
    elif action == 'delete':
        for name in names:
            btn.insert(InlineKeyboardButton(name, callback_data=f"tracker_confirm_{name}"))
    elif action == 'edit':
        for name in names:
            btn.insert(InlineKeyboardButton(name, callback_data=f"tracker_edit_{name}"))

    btn.row(InlineKeyboardButton(loc.B_BACK, callback_data="tracker_menu"))
    return btn


# Функція, яка генерує та повертає календар з переданими значеннями року та місяця
async def generate_calendar_buttons(user_id, year, month, tracker_name):
    calendar_buttons = InlineKeyboardMarkup(row_width=7)
    cal = calendar.monthcalendar(year, month)

    now = datetime.now()
    loc = await language_setup(user_id)

    # Встановлення локалі
    locale.setlocale(locale.LC_TIME, loc.LOC)

    # Додаємо заголовок з місяцем і роком
    calendar_buttons.row(InlineKeyboardButton(f"{calendar.month_name[month]} {year}", callback_data="ignore"))

    # Додаємо заголовки днів тижня
    calendar_buttons.row(*[InlineKeyboardButton(calendar.day_abbr[i], callback_data="ignore") for i in range(7)])

    # Додаємо дні місяця
    for week in cal:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(" ", callback_data="ignore"))
            else:
                # Перевіряємо, чи позначена кнопка
                start = sq.is_start_date(user_id, year, month, day, tracker_name)
                marked = sq.is_marked(user_id, year, month, day, tracker_name)
                active = now.year == year and now.month == month and now.day == day

                if start:
                    text = f"{day} 🟩" if marked else f"{day} 🟦"
                elif active:
                    text = f"{day} 🟢" if marked else f"{day} 🔴"
                else:
                    text = f"{day} ✅" if marked else str(day)

                row.append(InlineKeyboardButton(text, callback_data=f"calendar_{year}_{month}_{day}_{tracker_name}"))
        calendar_buttons.row(*row)

    # Додаємо кнопки для перемикання місяців
    calendar_buttons.row(
        InlineKeyboardButton("⬅️", callback_data=f"prevmonth_{tracker_name}"),
        InlineKeyboardButton("➡️", callback_data=f"nextmonth_{tracker_name}")
    )

    calendar_buttons.row(
        InlineKeyboardButton(loc.B_BACK, callback_data="back")
    )

    return calendar_buttons
