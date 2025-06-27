from src.localization import loc_eng
from src.localization import loc_s
from src.localization import loc_ua
import habitTrackerDataBase as sq

def get_loc(lang_code):
    if lang_code == 's':
        return loc_s
    elif lang_code in ('uk', 'ua'):
        return loc_ua
    else:
        return loc_eng

async def language_setup(user_id):
    lang_code = await sq.get_user_lang(user_id)
    return get_loc(lang_code)