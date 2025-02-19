from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
def start_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Создать папку', callback_data='create_folder'),InlineKeyboardButton(text='Загрузить файл', callback_data="upload_file")],
        [InlineKeyboardButton(text='Мои файлы', callback_data="my_files")]
    ])
def three(folders):
    buttons = []
    for i in range(0, len(folders)-1, 2):
        buttons.append([InlineKeyboardButton(text='📁' + folders[i].folder_name, callback_data=f'folder_{folders[i].id}'), InlineKeyboardButton(text='📁' + folders[i+1].folder_name, callback_data=f'folder_{folders[i+1].id}')])
    if len(folders) % 2 != 0:
        buttons.append([InlineKeyboardButton(text='📁' + folders[-1].folder_name, callback_data=f'folder_{folders[-1].id}')])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def actions_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Создать папку', callback_data='create_folder'),
         InlineKeyboardButton(text='Загрузить файл', callback_data="upload_file")],
        [InlineKeyboardButton(text='Назад', callback_data="back")]
    ])