HELP_COMMAND = """
<b>/start</b> - <em>Запустить бота</em>
<b>/help</b> - <em>Информация про команды</em>
<b>/menu</b> - <em>Главное меню трекеров</em>
<b>/unlogin</b> - <em>Удалить себя из базы данных</em>
<b>/language</b> - <em>Сменить язык</em>
"""

START = """
Добро пожаловать в бота!
Данный бот предназначен для создавания ваших трекеров привычек!
Для начала работы используйте - /menu
Для просмотра существующих команд - /help
"""

H_UNLOGIN_TRUE = "Вы уверены, что хотите удалить все свои записи?"

H_UNLOGIN_FALSE = "У вас и так нет никаких записей!\nДля создания, просто войдите в меню - /menu"

H_MENU = "Меню ваших трекеров, выберите опцию!"

H_MENU_LANGUAGE = "Выберите язык:"

H_NEW = "Введите название для вашего трекера:"

H_CHOISE_TRUE = "Выберите трекер!"

H_CHOISE_FALSE = "У вас пока нет трекеров :(\nПерейдите в меню, что бы создать новые!"

H_TRACKER_MENU = "Выберите опцию"

H_TRACKER_RENAME_TRUE = "Выберите трекер для переименования"

H_TRACKER_RENAME_FALSE = "У вас пока нет трекеров :(\nПерейдите в меню, что бы создать новые!"

H_PROFILE_DELETED = "Вас больше нет в базе данных!"

H_TRACKER_DELETE_TRUE = "Выберите трекер для удаления"

H_TRACKER_DELETE_FALSE = "У вас больше не осталось трекеров :(\nПерейдите в меню, что бы создать новые!"

def tracker_delete_confirm(tracker = ""):
    return f"Вы уверены, что хотите удалить трекер '{tracker}'?"

H_TRACKER_RENAME = "Введите новое название:"

def tracker_output(tracker = ""):
    return f"Трекер '{tracker}'"

H_TRACKER_CREATE_TRUE = "Похоже, у вас есть такой трекер... Введите другое название!"

def tracker_false(tracker = ""):
    return f"Готово! Ваш трекер '{tracker}' готов к использованию!"

H_STATE_DECLINE = "Ваше действие отменено, попробуйте еще раз!"

B_MAIN_YOUR_TRACKERS = "Ваши трекеры"

B_MAIN_MENU_TRACKERS = "Меню трекеров"

B_MAIN_CREATE_TRACKER = "Создать новый трекер"

B_CLOSE = "Закрыть"

B_TRACKER_DELETE = "Удалить трекер"

B_TRACKER_RENAME = "Изменить название"

B_BACK = "Назад"

B_YES = "Да"

B_NO = "Нет"

LOC = "ru_RU.UTF-8"

H_LOC_MENU = "Выберите язык:"

B_LOC_ENG = "Английский"
B_LOC_UA = "Украинский"
B_LOC_S = "Русский"

H_LOC_ANSWER = "Язык изменён ✅"

