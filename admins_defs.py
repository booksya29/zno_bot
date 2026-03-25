import json
from aiogram import Router, types
from aiogram.filters import Command

rt_admin = Router()


@rt_admin.message(Command('global_stats'))
async def global_stats_cmd(message: types.message):
    with open('System/admins.json') as f:
        admins = json.load(f)

    if message.from_user.id in admins:
        await message.answer('Ви адмін!!')
    else:
        await message.answer('У вас немає адмінки:(')