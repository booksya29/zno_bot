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


