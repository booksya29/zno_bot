from admins_defs import rt_admin
from user_defs import rt_users
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import json
import os, dotenv, asyncio
from aiogram.utils.keyboard import InlineKeyboardBuilder

dotenv.load_dotenv(dotenv.find_dotenv())

token = os.getenv('TOKEN')
bot = Bot(token=token)
dp = Dispatcher()
dp.include_routers(rt_admin, rt_users)

@dp.message(CommandStart())
async def start_cmd(message:types.message):
    builder = InlineKeyboardBuilder()
    builder.button(text='Обрати предмет!', callback_data='subject')
    builder.adjust(1)
    await message.answer('Привіт! Для того, щоб почати працювати обери предмет.', reply_markup = builder.as_markup(resize_keyboard = True))
    user_id = message.from_user.id
    with open('System/stats.json', 'rt', encoding='utf-8') as f:
        read = json.load(f)
        if str(user_id) in read:
            return
        else:
            with open('System/stats.json', 'rt', encoding='utf-8') as f:
                read = json.load(f)
                read[user_id] = {'wrong_answers':{}, 'cur_subject':None, 'all_questions':0, 'cur_id':None, 'cur_answer':None}
            with open('System/stats.json', 'wt', encoding='utf-8') as f:
                json.dump(read, f)                






async def start():
    await dp.start_polling(bot)
asyncio.run(start())