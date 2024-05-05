from aiogram_dialog import Dialog, LaunchMode

from src.dialogs.windows.menu.menu import MainMenuWin
from src.dialogs.windows.process.process import ChoiceProcessWin, SendProcessWin

# You need to register these dialogs in the __init__.py
MenuDLG = Dialog(MainMenuWin, launch_mode=LaunchMode.ROOT)
ProcessDLG = Dialog(ChoiceProcessWin, SendProcessWin, launch_mode=LaunchMode.SINGLE_TOP)
