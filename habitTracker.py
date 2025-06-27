import calendar
from aiogram import Bot, Dispatcher, executor, types
from datetime import datetime, timedelta
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import habitTrackerDataBase as sq
import buttons as butt
from src.localization.localization import language_setup
from src.token import TOKEN
from src.callbackdatas import language

# Ініціалізація сховища станів
storage = MemoryStorage()

# База
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

# Стан для імені нового трекера
class TrackerState(StatesGroup):
    waiting_for_tracker_name = State()


# Стан для меню
class MenuState(StatesGroup):
    menu = State()


# Стан для нового імені
class RenameState(StatesGroup):
    rename = State()


# -------------------------------------------------- ФУНКЦІЇ -----------------------------------------------------

# Стартап
async def startup(_):
    await sq.startup()


# -------------------------------------------- ХЕНДЛЕРИ ПОВІДОМЛЕНЬ ------------------------------------------------

@dp.message_handler(lambda message: message.text.startswith("/"), state=MenuState.menu)
async def block_commands_in_state(message: types.Message, state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id - 1)

    loc = await language_setup(message.from_user.id)

    await message.reply(loc.H_STATE_DECLINE, reply_markup=butt.get_help_buttons())
    await state.finish()

# Команда запуску бота
@dp.message_handler(commands=['start'], state='*')
async def command_start(message: types.Message):
    await message.delete()
    user_id = message.from_user.id
    loc = await language_setup(user_id)
    await message.answer(loc.START, reply_markup=butt.get_start_buttons())


# Команда виклику довідника команд
@dp.message_handler(commands=['help'], state='*')
async def command_help(message: types.Message):
    await message.delete()
    user_id = message.from_user.id
    loc = await language_setup(user_id)
    await message.answer(loc.HELP_COMMAND, reply_markup=butt.get_help_buttons(), parse_mode='HTML')


# Команда запиту на видалення користувача з бази даних
@dp.message_handler(commands=['unlogin'], state='*')
async def command_unlogin(message: types.Message):
    await message.delete()
    flag = await sq.check_user_exists(message.chat.id)
    user_id = message.from_user.id
    loc = await language_setup(user_id)
    if flag:
        await message.answer(loc.H_UNLOGIN_TRUE,
                             reply_markup=await butt.get_confirmation_delprofile_button(user_id))
    else:
        await message.answer(loc.H_UNLOGIN_TRUE,
                             reply_markup=butt.get_help_buttons())
    await MenuState.menu.set()


# Команда виклику головного меню
@dp.message_handler(commands=['menu'], state='*')
async def command_tracker_menu(message: types.Message):
    await message.delete()
    await sq.register(message.chat.id, message.from_user.language_code)
    user_id = message.from_user.id
    loc = await language_setup(user_id)
    await message.answer(loc.H_MENU,
                         reply_markup=await butt.get_menu_buttons(user_id))
    await MenuState.menu.set()

@dp.message_handler(commands=['language'], state='*')
async def command_loc_menu(message: types.Message):
    await message.delete()

    user_id = message.from_user.id
    loc = await language_setup(user_id)

    await message.answer(loc.H_LOC_MENU,
                         reply_markup=await butt.get_loc_buttons(user_id))
    await MenuState.menu.set()


# -------------------------------------------- CALLBACK-ЗАПИТИ ------------------------------------------------

# Callback, що реагує на натискання певної дати
@dp.callback_query_handler(lambda c: c.data.startswith('calendar'), state=MenuState.menu)
async def process_callback_tracker(callback: types.CallbackQuery):
    user_id = callback.message.chat.id
    _, year, month, day, tracker = callback.data.split('_')

    # Перевіряємо, чи дата позначена
    marked = sq.is_marked(user_id, int(year), int(month), int(day), tracker)
    if marked:
        await sq.unmark_day(user_id, int(year), int(month), int(day), tracker)
    else:
        await sq.mark_day(user_id, int(year), int(month), int(day), tracker)

    # Оновлюємо календар
    await callback.message.edit_reply_markup(
        await butt.generate_calendar_buttons(user_id, int(year), int(month), tracker))


# Callback, що реагує на кнопки, які не є датами
@dp.callback_query_handler(lambda c: c.data == 'ignore', state=MenuState.menu)
async def process_callback_tracker_ignore(callback: types.CallbackQuery):
    await callback.answer()


# Callback, що реагує на перегортання дати вперед
@dp.callback_query_handler(lambda c: c.data.startswith('nextmonth'), state=MenuState.menu)
async def process_callback_tracker_nextmonth(callback: types.CallbackQuery):
    _, tracker = callback.data.split('_')

    current_date = datetime.strptime(callback.message.reply_markup.inline_keyboard[0][0].text, "%B %Y")
    last_day = calendar.monthrange(current_date.year, current_date.month)[1]
    selected_date = datetime(current_date.year, current_date.month, last_day) + timedelta(days=1)

    await callback.message.edit_reply_markup(await butt.generate_calendar_buttons(callback.message.chat.id,
                                                                                  selected_date.year,
                                                                                  selected_date.month,
                                                                                  tracker))


# Callback, що реагує на перегортання дати назад
@dp.callback_query_handler(lambda c: c.data.startswith('prevmonth'), state=MenuState.menu)
async def process_callback_tracker_prevmonth(callback: types.CallbackQuery):
    _, tracker = callback.data.split('_')

    current_date = datetime.strptime(callback.message.reply_markup.inline_keyboard[0][0].text, "%B %Y")
    selected_date = current_date - timedelta(days=current_date.day)

    await callback.message.edit_reply_markup(await butt.generate_calendar_buttons(callback.message.chat.id,
                                                                                  selected_date.year,
                                                                                  selected_date.month,
                                                                                  tracker))


# Callback, вихід з головного меню
@dp.callback_query_handler(lambda c: c.data == 'close', state=MenuState.menu)
async def process_callback_tracker_menu_close(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await state.finish()


# Callback, повернення до головного меню
@dp.callback_query_handler(lambda c: c.data == 'back', state=MenuState.menu)
async def process_callback_tracker_menu_back(callback: types.CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    loc = await language_setup(user_id)
    await callback.message.edit_text(loc.H_MENU, reply_markup=await butt.get_menu_buttons(user_id))


# Callback, створення нового трекера
@dp.callback_query_handler(lambda c: c.data == 'new', state=MenuState.menu)
async def process_callback_tracker_new(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    loc = await language_setup(callback.from_user.id)
    await callback.message.answer(loc.H_NEW)
    await state.finish()
    await TrackerState.waiting_for_tracker_name.set()


# Callback, меню трекерів
@dp.callback_query_handler(lambda c: c.data == 'menu', state=MenuState.menu)
async def process_callback_tracker_menu(callback: types.CallbackQuery):
    await callback.answer()
    trackers = await sq.get_trackers(callback.message.chat.id)
    user_id = callback.from_user.id
    loc = await language_setup(user_id)
    if trackers:
        await callback.message.edit_text(loc.H_CHOISE_TRUE,
                                         reply_markup=await butt.generate_tracker_buttons(trackers,
                                                                                          'choise',
                                                                                          user_id))
    else:
        await callback.message.edit_text(loc.H_CHOISE_FALSE,
                                         reply_markup=await butt.generate_tracker_buttons(trackers,
                                                                                          'choise',
                                                                                          user_id))


# Callback, скасування видалення профілю
@dp.callback_query_handler(lambda c: c.data == 'profile_delete_decline', state=MenuState.menu)
async def process_callback_profile_delete_decline(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await state.finish()


# Callback, підтвердження видалення профілю
@dp.callback_query_handler(lambda c: c.data == 'profile_delete', state=MenuState.menu)
async def process_callback_profile_delete(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await sq.unlogin(callback.message.chat.id)
    loc = await language_setup(callback.from_user.id)
    await callback.message.answer(loc.H_PROFILE_DELETED)
    await state.finish()

# Callback, меню видалення трекерів
@dp.callback_query_handler(lambda c: c.data == 'tracker_menu', state=MenuState.menu)
async def process_callback_tracker_menu(callback: types.CallbackQuery):
    await callback.answer()
    user_id = callback.from_user.id
    loc = await language_setup(user_id)
    await callback.message.edit_text(loc.H_TRACKER_MENU, reply_markup=await butt.get_tracker_menu_buttons(user_id))

# Callback, видалення трекера
@dp.callback_query_handler(lambda c: c.data.startswith('tracker_delete'), state=MenuState.menu)
async def porcess_callback_tracker_delete(callback: types.CallbackQuery):
    await callback.answer()
    _, _, tracker = callback.data.split('_')
    await sq.remove_tracker(callback.message.chat.id, tracker)
    trackers = await sq.get_trackers(callback.message.chat.id)
    user_id = callback.from_user.id
    loc = await language_setup(user_id)
    if trackers:
        await callback.message.edit_text(loc.H_TRACKER_DELETE_TRUE,
                                         reply_markup=await butt.generate_tracker_buttons(trackers,
                                                                                          'delete',
                                                                                          user_id))
    else:
        await callback.message.edit_text(loc.H_TRACKER_DELETE_FALSE,
                                         reply_markup=await butt.generate_tracker_buttons(trackers,
                                                                                          'delete',
                                                                                          user_id))

# Callback, підтвердження видалення трекера
@dp.callback_query_handler(lambda c: c.data.startswith('tracker_confirm'), state=MenuState.menu)
async def porcess_callback_tracker_confirm(callback: types.CallbackQuery):
    await callback.answer()
    _, _, tracker = callback.data.split('_')
    user_id = callback.from_user.id
    loc = await language_setup(user_id)
    await callback.message.edit_text(loc.tracker_delete_confirm(tracker),
                                     reply_markup=await butt.get_confirmation_deltrack_button(tracker,
                                                                                              user_id))

# Callback, меню перейменування трекерів
@dp.callback_query_handler(lambda c: c.data == 'tracker_rename_menu', state=MenuState.menu)
async def process_callback_rename_menu(callback: types.CallbackQuery):
    await callback.answer()
    trackers = await sq.get_trackers(callback.message.chat.id)
    user_id = callback.from_user.id
    loc = await language_setup(user_id)
    if trackers:
        await callback.message.edit_text(loc.H_TRACKER_RENAME_TRUE,
                                         reply_markup=await butt.generate_tracker_buttons(trackers,
                                                                                          'edit',
                                                                                          user_id))
    else:
        await callback.message.edit_text(loc.H_TRACKER_RENAME_FALSE,
                                         reply_markup=await butt.generate_tracker_buttons(trackers,
                                                                                          'edit',
                                                                                          user_id))

# Callback, запит нового імені для трекера
@dp.callback_query_handler(lambda c: c.data.startswith('tracker_edit'), state=MenuState.menu)
async def porcess_callback_tracker_edit(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    _, _, tracker = callback.data.split('_')
    await callback.message.delete()
    loc = await language_setup(callback.from_user.id)
    await callback.message.answer(loc.H_TRACKER_RENAME)
    await state.finish()
    async with state.proxy() as data:
        data['tracker'] = tracker
    await RenameState.rename.set()


# Callback, виведення обраного трекера
@dp.callback_query_handler(lambda c: c.data.startswith('tracker'), state=MenuState.menu)
async def porcess_callback_tracker_show(callback: types.CallbackQuery):
    _, tracker = callback.data.split('_')
    now = datetime.now()
    user_id = callback.from_user.id
    loc = await language_setup(user_id)
    await callback.message.edit_text(loc.tracker_output(tracker),
                                     reply_markup=await butt.generate_calendar_buttons(user_id,
                                                                                       now.year,
                                                                                       now.month,
                                                                                       tracker))

# Команда виклику зміни мови
@dp.callback_query_handler(language.filter(), state=MenuState.menu)
async def process_loc_menu(callback: types.CallbackQuery, state: FSMContext, callback_data):
    user_id = callback.from_user.id

    lang_code = callback_data["language"]

    await sq.set_user_lang(user_id, lang_code)

    loc = await language_setup(user_id)

    await callback.answer(loc.H_LOC_ANSWER)

    new_text = loc.H_LOC_MENU
    new_markup = await butt.get_loc_buttons(user_id)

    if callback.message.text != new_text or callback.message.reply_markup != new_markup:
        await callback.message.edit_text(new_text, reply_markup=new_markup)
    else:
        await callback.answer(loc.H_LOC_ANSWER)

# -------------------------------------------- МАШИНИ СТАНІВ ------------------------------------------------

# Стан: очікує введення імені нового трекера
@dp.message_handler(state=TrackerState.waiting_for_tracker_name)
async def process_state_tracker_name(message: types.Message, state: FSMContext):
    now = datetime.now()

    tracker = message.text
    trackers = await sq.get_trackers(message.chat.id)

    user_id = message.from_user.id
    loc = await language_setup(message.from_user.id)

    if tracker in trackers:
        await message.reply(loc.H_TRACKER_CREATE_TRUE)
        return

    await sq.add_tracker(message.chat.id, tracker)
    await state.finish()

    await MenuState.menu.set()
    await message.answer(loc.tracker_false(tracker))
    await message.answer(loc.tracker_output(tracker),
                         reply_markup=await butt.generate_calendar_buttons(user_id,
                                                                           now.year,
                                                                           now.month,
                                                                           tracker))


# Стан для меню, щоб користувач не міг викликати два меню одночасно
@dp.message_handler(state=MenuState.menu)
async def process_state_menu(message: types.Message, state: FSMContext):
    await bot.delete_message(message.chat.id, message.message_id - 1)

    loc = await language_setup(message.from_user.id)

    await message.reply(loc.H_STATE_DECLINE, reply_markup=butt.get_help_buttons())
    await state.finish()


# Стан для перейменування трекера
@dp.message_handler(state=RenameState.rename)
async def process_state_edit(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        tracker = data['tracker']

    tracker_name = message.text
    trackers = await sq.get_trackers(message.chat.id)

    user_id = message.from_user.id

    loc = await language_setup(user_id)
    if tracker_name in trackers:
        await message.reply(loc.H_TRACKER_CREATE_TRUE)
        return

    await sq.rename_tracker(message.chat.id, tracker, tracker_name)
    await state.finish()

    await MenuState.menu.set()
    await message.answer(loc.tracker_false(tracker_name))
    trackers = await sq.get_trackers(message.chat.id)
    if trackers:
        await message.answer(loc.H_TRACKER_RENAME_TRUE,
                             reply_markup=await butt.generate_tracker_buttons(trackers,
                                                                              'edit',
                                                                              user_id))
    else:
        await message.answer(loc.H_TRACKER_RENAME_FALSE,
                             reply_markup=await butt.generate_tracker_buttons(trackers,
                                                                              'edit',
                                                                              user_id))

# Мейн
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=startup)
