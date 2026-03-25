import requests
from bs4 import BeautifulSoup
import json
from System.subject_list import subjects
from random import randint
from pylatexenc.latex2text import LatexNodes2Text

def get_soup_file(id):
    with open('System\\stats.json', 'rt', encoding='utf-8') as f:
        read = json.load(f)
        cur_subject = read[str(id)]['cur_subject']
        if cur_subject == None:
            return None
        url_subject = subjects[cur_subject]['url']
        max_task = subjects[cur_subject]['tasks']
        random_task = randint(0, int(max_task))
        url = url_subject + str(random_task)
        print(f'Сайт {url}')
        conn = requests.get(url)
        if conn.status_code != 200:
            print(f'Немає підключення. Помилка: {conn.status_code}')
        soup = BeautifulSoup(conn.text, 'lxml')
        read[str(id)]['all_questions'] += 1
        with open('System\\stats.json', 'wt', encoding='utf-8') as f:
            json.dump(read, f)
        return soup, random_task

def get_question(soup):
    qurent_test = soup.find('form', class_="q-test")
    question_block = qurent_test.find('div', class_='question')
    video = None
    img = None
    if question_block.find('iframe'):
        video = question_block.find('iframe').get('src')
    
    if question_block.find('img'):
        img = 'https://zno.osvita.ua/' + question_block.find('img').get('src')
    text = question_block.text
    print(f'Фото: {img}')
    return text, img, video

def get_answers(soup):
    img_dict = None
    qurent_test = soup.find('form', class_='q-test')
    if qurent_test is None:
        return None, None
    answers_block_list = qurent_test.find_all('div', class_='answers')
    if len(answers_block_list) == 0:
        return None, None
    answers_list = qurent_test.find_all('div', class_='answer')
    if len(answers_block_list) == 0:
        return None, None
    if qurent_test.find('img'):
        img_dict = {}
        for answer in answers_list:
            if answer.find('img'):
                img_dict[answer.text] = answer.find('img').get('src')
    answer_list = list(answer_l.text for answer_l in answers_list)
    print(f"img_dict is {img_dict}")
    return answer_list, img_dict

def get_right_answer(soup):
    q_block=soup.find('form', class_="q-test")
    result = q_block.find('input', {'type':"hidden", 'name':'result'}).get('value')
    print(f'Правильний результат {result}')
    return result

import random

def generate_wrong_answers(correct: str):
    # correct = "1a;2b;3c;4d"
    pairs = correct.split(";")  # ["1a", "2b", "3c", "4d"]
    
    numbers = [p[0] for p in pairs]  # ["1", "2", "3", "4"]
    letters = [p[1] for p in pairs]  # ["a", "b", "c", "d"]
    
    wrong_answers = []
    while len(wrong_answers) < 3:
        shuffled = letters.copy()
        random.shuffle(shuffled)
        variant = ";".join(n + l for n, l in zip(numbers, shuffled))
        
        # щоб не повторювались і не співпадали з правильною
        if variant != correct and variant not in wrong_answers:
            wrong_answers.append(variant)
    
    return wrong_answers

def wrong_answer_generate_free_form(correct):
    wrong_list=[]
    wrong_list.append(float(correct))
    def minus(wrong):
        return float(correct)-float(wrong)
    def plus(wrong):
        return float(correct)+float(wrong)
    while len(wrong_list)<4:
        c_def = random.choice([minus,plus])
        number_for_add = random.randint(1,10)
        wrong_answer=c_def(number_for_add)
        if wrong_answer in wrong_list:
            pass
        else:
            wrong_list.append(wrong_answer)
    wrong_list.sort()
    return wrong_list

def get_explanation(id):
    with open('System\\stats.json', 'rt', encoding='utf-8') as f:
        cur_stats = json.load(f)[str(id)]
    url_head = subjects[cur_stats['cur_subject']]['url']
    url = url_head + str(cur_stats['cur_id'])
    conn = requests.get(url)
    soup = BeautifulSoup(conn.text, 'lxml')
    img = None
    q_test=soup.find('form', class_='q-test')
    explanation_block = q_test.find('div', class_='explanation')
    if explanation_block:
        if explanation_block.find_all('img'):
            img = ('https://zno.osvita.ua'+str(img_u) for img_u in explanation_block.find_all('img'))
        if img:
            return explanation_block.text, list(img)
        else:
            return explanation_block.text, None
    else:
        return None, None

# conn = requests.get('https://zno.osvita.ua/mathematics/all/481/')
# soup = BeautifulSoup(conn.text, 'lxml')

