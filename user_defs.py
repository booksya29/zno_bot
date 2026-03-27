from aiogram import Router, types
from aiogram import F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from System.subject_list import subjects
import json, parsing, os
from random import randint
from pylatexenc.latex2text import LatexNodes2Text
from base_class import Father_task
rt_users = Router()


@rt_users.callback_query(F.data == 'subject')
async def subject_cmd(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    for i in subjects.keys():
        builder.button(text=i, callback_data='subject'+i)
    builder.adjust(2)
    await callback.message.answer('Обери предмет:', reply_markup = builder.as_markup())
    await callback.answer('', )


@rt_users.callback_query(F.data.startswith('subject'))
async def subject_button(callback: types.CallbackQuery):
    subject = callback.data[7:]
    builder = ReplyKeyboardBuilder()
    builder.button(text='Наступне запитання!')
    builder.button(text='Налаштування')
    await callback.message.answer(f'Чудово. Ви обрали предмет: {subject}', reply_markup=builder.as_markup(resize_keyboard=True))
    await callback.answer('Обрано!')
    with open(os.path.join('System', 'stats.json'), 'rt', encoding='utf-8') as f:
        read = json.load(f)
    read[str(callback.from_user.id)]['cur_subject'] = subject
    with open(os.path.join('System', 'stats.json'), 'wt', encoding='utf-8') as f:
        json.dump(read, f)



@rt_users.callback_query(F.data == 'stats')
async def stats_cmd(callback: types.callback_query):
    with open(os.path.join('System', 'stats.json'), 'rt', encoding='utf-8') as f:
        read = json.load(f)[str(callback.from_user.id)]
        if read['all_questions'] > 0:
            await callback.message.answer(f'Ваша статистика: \nВи відповіли на {read['all_questions']} запитань. \nЗ яких неправильно: {dict(read['wrong_answers'])} питань\nВідсоток правильних:{(int(read['all_questions']) - len(read['wrong_answers'].values())/int(read['all_questions'])) * 100}%')
            await callback.answer('')
        else:
            await callback.message.answer('На жаль, ви ще не пройшли жодного тесту.\nСтатистика не зібрана')
            await callback.answer('')


@rt_users.message(F.text == 'Налаштування')
async def settings_cmd(message:types.message):
    builder = InlineKeyboardBuilder()
    builder.button(text='Змінити предмет', callback_data='subject')
    builder.button(text='Статистику', callback_data='stats')
    await message.answer('Налаштування:', reply_markup = builder.as_markup())


@rt_users.message(F.text == 'Наступне запитання!')
async def next_cmd(message: types.Message):
    chat_id = message.from_user.id
    task = Father_task(chat_id)
    task.parsing()
    task =task.class_select()
    if task is None:
        await message.answer('Цей тип завдання поки не підтримується. Спробуй ще раз!')
        return
    await task.answer_question_callback(message)


@rt_users.callback_query(F.data=='47293856')
async def true_answ(callback:types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    
    builder.button(text='Подивитись пояснення!', callback_data='explanation')
    await callback.message.answer('Правильна відповідь!', reply_markup = builder.as_markup())
    await callback.answer('')


@rt_users.callback_query(F.data=='47293156')
async def false_answ(callback:types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.button(text='Подивись пояснення!', callback_data='explanation')
    await callback.message.answer('Неправильна відповідь.', reply_markup=builder.as_markup())
    await callback.answer('')
    chat_id = callback.from_user.id
    with open(os.path.join('System', 'stats.json'), 'rt', encoding='utf-8') as f:
        read = json.load(f)
        cur_id = read[str(chat_id)]['cur_id']
        cur_subject = read[str(chat_id)]['cur_subject']
    try:
        read[str(chat_id)]['wrong_answers'][cur_subject].append(cur_id)
    except KeyError:
        read[str(chat_id)]['wrong_answers'][cur_subject] = []
        read[str(chat_id)]['wrong_answers'][cur_subject].append(cur_id)
    with open(os.path.join('System', 'stats.json'), 'wt', encoding='utf-8') as f:
        json.dump(read,f)
@rt_users.callback_query(F.data == 'explanation')
async def explanation_print(callback: types.CallbackQuery):
    convert = LatexNodes2Text()
    chat_id = callback.from_user.id
    text_exp_math, img_exp = parsing.get_explanation(int(chat_id))
    if text_exp_math:
        text_exp = convert.latex_to_text(text_exp_math)
        await callback.message.answer(text_exp)
        if img_exp:
            for i in img_exp:
                await callback.message.answer_photo(photo=i)
    else:
        await callback.message.answer('На жаль, пояснення для цього питання на сайті немає! :(')
    await callback.answer('')