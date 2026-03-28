import requests
from bs4 import BeautifulSoup
import json
from System.subject_list import subjects
from random import randint
from pylatexenc.latex2text import LatexNodes2Text
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



def get_explanation(chat_id):
    """Повертає (text, images) пояснення для поточного завдання користувача."""
    try:
        with open('System/stats.json', 'rt', encoding='utf-8') as f:
            read = json.load(f)
        data = read[str(chat_id)]
        cur_id = data.get('cur_id')
        cur_subject = data.get('cur_subject')
        if not cur_id or not cur_subject:
            return None, None
        url = subjects[cur_subject]['url'] + str(cur_id)
        conn = requests.get(url)
        if conn.status_code != 200:
            return None, None
        soup = BeautifulSoup(conn.text, 'lxml')
        explanation_div = soup.find('div', class_='explanation')
        if not explanation_div:
            return None, None
        # Витягуємо текст (може містити LaTeX)
        text = explanation_div.get_text(separator=' ', strip=True)
        # Витягуємо зображення
        imgs = []
        for img in explanation_div.find_all('img'):
            src = img.get('src')
            if src:
                imgs.append(src)
        return text if text else None, imgs if imgs else None
    except Exception as e:
        print(f'[get_explanation error]: {e}')
        return None, None
