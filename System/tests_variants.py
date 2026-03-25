from random import randint
question_4 = ['a','e','c','d','e']
a = [2,55,1,4,623]
question_4.sort()
question_4_answers_list = []
print(len(question_4))
while True:
    if len(question_4_answers_list) == 4:
        break
    index =randint(0,4)
    if question_4[index] in question_4_answers_list:
        pass
    else:
        question_4_answers_list.append(question_4[index])
print(question_4_answers_list)