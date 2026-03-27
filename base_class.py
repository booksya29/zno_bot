import requests
from bs4 import BeautifulSoup
import os, json
from random import randint
from System.subject_list import subjects

from playwright.async_api import async_playwright
class Father_task():
    def __init__(self, chat_id):
        #Відносяться до питання
        self.base_url = None 
        self.number_task = None #
        self.task_type = None #
      
        self.current_subject = None #
        self.chat_id = chat_id #
        self.true_answer = None

    
    def parsing(self):
        self.get_current_subject()
        self.generate_number_task()
        self.base_url_get()
        self.url = self.base_url + str(self.number_task)
        conn = requests.get(self.url)
        if conn.status_code != 200:
            print(f'На жаль, підключення до сайту немає.({conn.status_code})')
            return
        soup = BeautifulSoup(conn.text, 'lxml')
        self.soup = soup
        self.get_task_type()
    
    def base_url_get(self):
        self.base_url = subjects[self.current_subject]['url']

    def generate_number_task(self):
        max_task = subjects[self.current_subject]['tasks']
        self.number_task = randint(0, int(max_task))


    def get_task_type(self):
        q_test = self.soup.find('form', class_='q-test')
        desc_text = q_test.find('div', class_='description').get_text()
        known_types = [
            'Завдання з вибором однієї правильної відповіді',
            'Завдання відкритої форми з короткою відповіддю (1 вид)',
            'Завдання на встановлення відповідності (логічні пари)',
        ]
        self.task_type = None
        for t in known_types:
            if t in desc_text:
                self.task_type = t
                break
        self.true_answer = q_test.find('input', attrs={'name': 'result'}).get('value')
    
    def get_current_subject(self):
        f_path = os.path.join('System', 'stats.json')
        with open(f_path, 'rt', encoding='utf-8') as f:
            self.current_subject = json.load(f)[str(self.chat_id)]['cur_subject']
    
    def class_select(self):
        from types_classes import que_cor_1, free_form_que_1, sequence_que
        if self.task_type == 'Завдання з вибором однієї правильної відповіді':
            obj = que_cor_1(self.chat_id)
        elif self.task_type == 'Завдання відкритої форми з короткою відповіддю (1 вид)':
            obj = free_form_que_1(self.chat_id)
        elif self.task_type == 'Завдання на встановлення відповідності (логічні пари)':
            obj = sequence_que(self.chat_id)
        else:
            print(f'[НЕВІДОМИЙ ТИП]: "{self.task_type}"')
            return None
        obj.soup = self.soup
        obj.url = self.url
        obj.task_type = self.task_type
        obj.true_answer = self.true_answer
        obj.number_task = self.number_task
        return obj


    async def get_task_photo(self):
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            context = await browser.new_context()
            page = await context.new_page()
            await page.goto(self.url)
            self.photo = await page.locator('form[class="q-test"]').screenshot()
            await browser.close()