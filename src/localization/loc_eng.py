HELP_COMMAND = """
<b>/start</b> - <em>Launch the bot</em>
<b>/help</b> - <em>Information about the commands</em>
<b>/menu</b> - <em>Main tracker menu</em>
<b>/unlogin</b> - <em>Delete yourself from the database</em>
<b>/language</b> - <em>Change language</em>
"""

START = """
Welcome to the bot!
This bot is designed to help you create and manage habit trackers!
To get started, use /menu  
To view available commands, use /help
"""

H_UNLOGIN_TRUE = "Are you sure you want to delete all your records?"

H_UNLOGIN_FALSE = "You don't have any records yet!\nTo create one, just go to the menu: /menu"

H_MENU = "Your tracker menu, choose an option!"

H_NEW = "Enter a name for your tracker:"

H_CHOISE_TRUE = "Choose a tracker!"

H_CHOISE_FALSE = "You don't have any trackers yet :(\nGo to the menu to create a new one!"

H_TRACKER_MENU = "Choose an option"

H_TRACKER_RENAME_TRUE = "Choose a tracker to rename"

H_TRACKER_RENAME_FALSE = "You don't have any trackers yet :(\nGo to the menu to create a new one!"

H_PROFILE_DELETED = "You have been removed from the database!"

H_TRACKER_DELETE_TRUE = "Choose a tracker to delete"

H_TRACKER_DELETE_FALSE = "You have no trackers left :(\nGo to the menu to create a new one!"


def tracker_delete_confirm(tracker=""):
    return f"Are you sure you want to delete the tracker '{tracker}'?"


H_TRACKER_RENAME = "Enter a new name:"


def tracker_output(tracker=""):
    return f"Tracker '{tracker}'"


H_TRACKER_CREATE_TRUE = "Looks like you already have a tracker with that name... Enter a different one!"


def tracker_false(tracker=""):
    return f"Done! Your tracker '{tracker}' is ready to use!"


H_STATE_DECLINE = "Action canceled, please try again!"

B_MAIN_YOUR_TRACKERS = "Your Trackers"

B_MAIN_MENU_TRACKERS = "Tracker Menu"

B_MAIN_CREATE_TRACKER = "Create New Tracker"

B_CLOSE = "Close"

B_TRACKER_DELETE = "Delete Tracker"

B_TRACKER_RENAME = "Rename"

B_BACK = "Back"

B_YES = "Yes"

B_NO = "No"

LOC = "en_US.UTF-8"

H_LOC_ANSWER = "Language changed ✅"

B_LOC_ENG = "English"
B_LOC_UA = "Ukrainian"

H_LOC_MENU = "Choose a language:"