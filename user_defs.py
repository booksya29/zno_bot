from aiogram import Router, types
from aiogram import F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from System.subject_list import subjects
import json, parsing
from random import randint
from pylatexenc.latex2text import LatexNodes2Text
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
    with open('System/stats.json', 'rt', encoding='utf-8') as f:
        read = json.load(f)
    read[str(callback.from_user.id)]['cur_subject'] = subject
    with open('System/stats.json', 'wt', encoding='utf-8') as f:
        json.dump(read, f)



@rt_users.callback_query(F.data == 'stats')
async def stats_cmd(callback: types.callback_query):
    with open('System/stats.json', 'rt', encoding='utf-8') as f:
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
async def next_cmd(message:types.message):
    question_4 = ['a','b','c','d','e']
    converter = LatexNodes2Text()
    chat_id = message.from_user.id
    soup, id = parsing.get_soup_file(chat_id)
    with open('System/stats.json', 'rt') as f:
        read = json.load(f)
        read[str(chat_id)]['cur_id'] = int(id)
    with open('System/stats.json', 'wt') as w:
        json.dump(read,w)
    if soup == None:
        builder = InlineKeyboardBuilder()
        builder.button(text='Обрати предмет:', callback_data='subject')
        await message.answer('Ви не обрали предмет!', reply_markup = builder.as_markup())
        return
    text_math, image, video = parsing.get_question(soup)
    text = converter.latex_to_text(text_math)
    if video != None:
        await message.answer(video)
    if image != None:
        try:
            await message.answer_photo(photo = image, caption = text)
        except:
            await message.answer_photo(photo = image, caption = text)
            await message.answer(text[:int(len(text)/4)])
            await message.answer(text[int(len(text)/4) : int(len(text)/2)])
            await message.answer(text[int(len(text)/2) : ] )
    else:
        try:
            await message.answer(text)
        except:
            await message.answer(text[:int(len(text)/4)])
            await message.answer(text[int(len(text)/4) : int(len(text)/2)])
            await message.answer(text[int(len(text)/2) : ] )
    answer_list_math, img_dict = parsing.get_answers(soup)
    answer_list = []
    if answer_list_math:
        for i in answer_list_math:
            answer_list.append(converter.latex_to_text(i))
    true_answer = parsing.get_right_answer(soup)
    print(f'answer_list = {answer_list}')
    if answer_list:
        if len(answer_list) == 4 or len(answer_list)==5:
                builder = InlineKeyboardBuilder()
                for i in answer_list:
                    if i[0].replace('А', 'a').replace('Б', 'b').replace('В','c').replace('Г', 'd').replace('Д', 'e') == true_answer:
                        builder.button(text=i[0]+') ' + i[1:], callback_data='47293856')
                    else:
                        builder.button(text=i[0]+') ' + i[1:], callback_data='47293156')
                builder.adjust(1)
                await message.answer('Обери правильну відповідь!', reply_markup=builder.as_markup())
        elif len(answer_list) == 0 and true_answer in ['a','b','c','d','e']:
            builder=InlineKeyboardBuilder()
            for i in question_4:
                if i != true_answer:
                    builder.button(text=i, callback_data='47293156')
                else:
                    builder.button(text=i, callback_data='47293856')
            await message.answer('Оберіть правильну відповідь!', reply_markup=builder.as_markup())
        elif len(answer_list) == 8 or len(answer_list) == 9:
            builder = InlineKeyboardBuilder()
            if img_dict:
                for i in img_dict.keys():
                    await message.answer_photo(photo=img_dict[i], caption=i)
                for i in answer_list:
                    if i[0] in img_dict.keys():
                        pass
                    else:
                        await message.answer(i[0]+ ') '+  i[1:])
            else:
                for i in answer_list:
                    await message.answer(i[0]+ ') '+  i[1:])
            wrong_answers = parsing.generate_wrong_answers(true_answer)
            builder = InlineKeyboardBuilder()
            for i in wrong_answers:
                builder.button(text = i,callback_data='47293156')
            builder.button(text = true_answer,callback_data='47293856')
                
            await message.answer('Обери правильну відповідь!', reply_markup=builder.as_markup())
    elif answer_list is None:
        true_answers_list = true_answer.split(';')
        if len(true_answers_list) == 1:
            builder = InlineKeyboardBuilder()
            answers_list = parsing.wrong_answer_generate_free_form(true_answer)
            for answer in answers_list:
                if float(answer) == float(true_answer):
                    builder.button(text=str(answer),callback_data='47293856')
                else:
                    builder.button(text=str(answer), callback_data='47293156')
            builder.adjust(1)
            await message.answer('Обери правильну відповідь!', reply_markup=builder.as_markup())
        true_answers_list = true_answer.split(';')
        if len(true_answers_list) ==2:
            builder = InlineKeyboardBuilder()
            for true_answer in true_answers_list:
                answer_list = parsing.wrong_answer_generate_free_form(true_answer)
                for answer in answer_list:
                    if float(answer) == float(true_answer):
                        builder.button(text=answer, callback_data='47293856')
                    else:
                        builder.button(text=answer, callback_data='47293156')

    elif len(answer_list) == 0:
        builder = InlineKeyboardBuilder()
        answer_list_elements = list(true_answer.split(';'))
        if true_answer is 'a' or true_answer == 'b' or true_answer == 'c' or true_answer == 'd' or true_answer == 'e':
            builder = InlineKeyboardBuilder()
            for i in question_4:
                if i == true_answer:
                    builder.button(text=i, callback_data='47293856')
                else:
                    builder.button(text=i, callback_data='47293156')
            await message.answer('Обери відповідь!', reply_markup=builder.as_markup())
        if len(answer_list_elements) == 1:
            list_answers = parsing.wrong_answer_generate_free_form(true_answer)
            for i in list_answers:
                if i == float(true_answer):
                    builder.button(text=str(i), callback_data='47293856')
                else:
                    builder.button(text=str(i), callback_data='47293156')
                builder.adjust(2)
            await message.answer('Оберіть правильну відповідь!', reply_markup=builder.as_markup())
        else:
            builder = InlineKeyboardBuilder()
            answers = parsing.wrong_answer_generate_free_form(true_answer)
            answers.append(true_answer)
            answers.sort()
            for answer in answers:
                if answer == true_answer:
                    builder.button(text=answer, callback_data='47293856')
                else:
                    builder.button(text=answer, callback_data='47293156')
            await message.answer('Обери відповідь!', reply_markup=builder.as_markup())
            


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
    with open('System/stats.json', 'rt', encoding='utf-8') as f:
        read = json.load(f)
        cur_id = read[str(chat_id)]['cur_id']
        cur_subject = read[str(chat_id)]['cur_subject']
    try:
        read[str(chat_id)]['wrong_answers'][cur_subject].append(cur_id)
    except KeyError:
        read[str(chat_id)]['wrong_answers'][cur_subject] = []
        read[str(chat_id)]['wrong_answers'][cur_subject].append(cur_id)
    with open('System/stats.json', 'wt', encoding='utf-8') as f:
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