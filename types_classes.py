from base_class import Father_task
from aiogram import types, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder
import parsing

class que_cor_1(Father_task):
    def __init__(self, chat_id):
        super().__init__(chat_id)
        self.letters_list = ['a','b','c','d','e']
    
    async def answer_question_callback(self, message: types.Message):
        builder = InlineKeyboardBuilder()
        for i in self.letters_list:
            if i == self.true_answer:
                builder.button(text=i, callback_data='47293856')
            else:
                builder.button(text=i, callback_data='47293156')
        loading_msg = await message.answer(text='Починаю завантажувати фото...')
        self.get_task_photo()
        await loading_msg.delete()
        await message.answer_photo(photo=types.BufferedInputFile(file = self.photo, filename = 'task.png'), caption='Оберіть правильну відповідь!', reply_markup=builder.as_markup())

class free_form_que_1(Father_task):
    def __init__(self, chat_id):
        super().__init__(chat_id)
    
    async def answer_question_callback(self, message: types.Message):
        answer_list = parsing.wrong_answer_generate_free_form(self.true_answer)
        builder = InlineKeyboardBuilder()
        for i in answer_list:
            if float(i) == float(self.true_answer):
                builder.button(text=str(i), callback_data='47293856')
            else:
                builder.button(text = str(i), callback_data='47293156')
        load_message = await message.answer(text='Починаю завантажувати фото...')
        self.get_task_photo()
        await load_message.delete()
        await message.answer_photo(photo=types.BufferedInputFile(file=self.photo, filename='task.png'), caption='Оберіть правильну відповідь!', reply_markup=builder.as_markup())

class sequence_que(Father_task):
    def __init__(self, chat_id):
        super().__init__(chat_id)
    
    async def answer_question_callback(self, message: types.Message):
        answers_list = parsing.generate_wrong_answers(self.true_answer)
        answers_list.append(self.true_answer)
        builder = InlineKeyboardBuilder()
        for i in answers_list:
            if i == self.true_answer:
                builder.button(text=str(i), callback_data='47293856')
            else:
                builder.button(text=str(i), callback_data='47293156')
        message_load = await message.answer(text='Починаю завантажувати фото...')
        self.get_task_photo()
        await message_load.delete()
        await message.answer_photo(photo=types.BufferedInputFile(file=self.photo, filename='task.png'), caption= 'Оберіть правильну відповідь!', reply_markup=builder.as_markup())