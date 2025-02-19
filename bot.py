from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
import asyncio
from config import TOKEN
from keyboards import start_keyboard, three, actions_keyboard
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from models import SessionLocal, Folder, User, File
from sqlalchemy import and_

API_TOKEN = TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher()


class BotState(StatesGroup):
    waiting_folder_name = State()
    waiting_file = State()
    into_folder = State()

#Command handlers
#/start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    db = SessionLocal()
    try:
        if not(db.query(User).filter(User.user_id == message.from_user.id).first()):
            user = User(user_id=message.from_user.id, username=message.from_user.username)
            db.add(user)
            db.commit()
    finally:
        db.close()
    await message.answer(f"Привет, {message.from_user.full_name}! Я твой файловый менеджер. С чего начнём?", reply_markup=start_keyboard())

@dp.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("Я бот-файловый менеджер. Используй /start, чтобы начать.")

@dp.message(Command("info"))
async def cmd_info(message: Message):
    await message.answer("Я бот для управления файлами. Создай папку и начни загружать файлы!")

#Callback handlers
@dp.callback_query(F.data == 'create_folder')
async def get_folder_name(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Напишите название папки')
    await state.set_state(BotState.waiting_folder_name)
    await callback.answer()

@dp.callback_query(F.data == 'my_files')
async def my_files(callback: CallbackQuery, state: FSMContext):
    db = SessionLocal()
    try:
        userid = db.query(User).filter(User.user_id == callback.from_user.id).first().id
        folders = db.query(Folder).filter(Folder.user_id == userid).all()
        await callback.message.answer(text='Ваши папки:', reply_markup=three(folders))
    finally:
        db.close()

    await callback.answer()

@dp.callback_query(F.data == 'upload_file')
async def get_file(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Скиньте файл или текст, которое хотите сохранить')
    await state.set_state(BotState.waiting_file)
    await callback.answer()

@dp.callback_query(F.data.startswith('folder_'))
async def enter_folder(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BotState.into_folder)
    await state.update_data(current_folder_id=callback.data.split('_')[1])
    await callback.answer()
    db = SessionLocal()
    try:
        await callback.message.answer(text=f'Вы выбрали папку {db.query(Folder).filter(Folder.id == callback.data.split("_")[1]).first().folder_name}')
        files = db.query(File).filter(File.folder_id == callback.data.split('_')[1]).all()
        chat_id = callback.from_user.id
        for el in files:
            await bot.forward_message(chat_id=chat_id, from_chat_id=chat_id, message_id=el.file_id)
        await callback.message.answer(text='Выберите действие:', reply_markup=actions_keyboard())
    finally: pass

@dp.callback_query(F.data == 'back')
async def back(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()

#States handlers
@dp.message(BotState.waiting_folder_name)
async def create_folder(message: Message, state: FSMContext):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == message.from_user.id).first()
        if not(db.query(Folder).filter(
                and_(
                    Folder.folder_name == message.text,
                    Folder.user_id == user.id
                )).first()):
            folder = Folder(user_id=user.id, folder_name=message.text)
            db.add(folder)
            db.commit()
            await message.answer(f'Папка {message.text} успешно создана')
        else:
            await message.answer('Папка с таким названием уже существует')
    finally:
        db.close()
    await state.clear()

@dp.message(BotState.waiting_file)
async def upload_file(message: Message, state: FSMContext):
    db = SessionLocal()
    try:
        data = await state.get_data()
        file = File(file_id=message.message_id, folder_id=data.get('current_folder_id'))
        db.add(file)
        db.commit()
        await message.answer("Файл успешно загружен")
    except:
        await message.answer('Cначала выберите папку, в которую хотите сохранить файл')
    finally:
        db.close()
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())