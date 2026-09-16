#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TP TL1: implémentation des automates
"""

import sys

###############
# Cadre général

V = set(('.', 'e', 'E', '+', '-')
        + tuple(str(i) for i in range(10)))

class Error(Exception):
    pass

INPUT_STREAM = sys.stdin
END = '\n' # WARNING: test_tp modifies the value of END.

# Initialisation: on vérifie que END n'est pas dans V
def init_char():
    if END in V:
        raise Error('character ' + repr(END) + ' in V')

# Accès au caractère suivant dans l'entrée
def next_char():
    global INPUT_STREAM
    ch = INPUT_STREAM.read(1)
    # print("@", repr(ch))  # decommenting this line may help debugging
    if ch in V or ch == END:
        return ch
    raise Error('character ' + repr(ch) + ' unsupported')


############
# Question 1 : fonctions nonzerodigit et digit

def nonzerodigit(char):
    assert (len(char) <= 1)
    return '1' <= char <= '9'

def digit(char):
    assert (len(char) <= 1)
    return '0' <= char <= '9'


############
# Question 2 : integer et pointfloat sans valeur

def integer_Q2():
    init_char()
    return integer_Q2_state_0()


def integer_Q2_state_0():
    ch = next_char()
    if nonzerodigit(ch):
        return integer_Q2_state_2()
    elif ch == END:
        return False
    elif digit(ch):
        return integer_Q2_state_1()
    else:
        return False

def integer_Q2_state_1():
    ch = next_char()
    if nonzerodigit(ch):
        return False
    elif ch == END:
        return True
    elif digit(ch):
        return integer_Q2_state_1()
    else:
        return False

def integer_Q2_state_2():
    ch = next_char()
    if digit(ch):
        return integer_Q2_state_2()
    elif ch == END:
        return True
    else:
        return False

def pointfloat_Q2():
    init_char()
    return pointfloat_Q2_state_0()

# Définir ici les fonctions manquantes

def pointfloat_Q2_state_0():
    ch=next_char()
    if digit(ch):
        return pointfloat_Q2_state_2()
    elif ch == '.':
        return pointfloat_Q2_state_1()
    else:
        return False


def pointfloat_Q2_state_1():
    ch=next_char()
    if digit(ch):
        return pointfloat_Q2_state_3()
    else:
        return False


def pointfloat_Q2_state_3():
    ch=next_char()
    if digit(ch):
        return pointfloat_Q2_state_3()
    if ch == END:
        return True
    else:
        return False


def pointfloat_Q2_state_2():
    ch=next_char()
    if digit(ch):
        return pointfloat_Q2_state_2()
    elif ch == '.':
        return pointfloat_Q2_state_3()
    else:
        return False


############
# Question 5 : integer avec calcul de la valeur
# si mot accepté, renvoyer (True, valeur)
# si mot refusé, renvoyer (False, None)

# Variables globales pour se transmettre les valeurs entre états
int_value = 0
exp_value = 0


def integer():
    init_char()
    return integer_state_0()


def integer_state_0():
    global int_value
    int_value=0
    ch = next_char()
    if nonzerodigit(ch):
        int_value = int(ch)
        return integer_state_2()
    elif ch == END:
        return (False, None)
    elif digit(ch):
        return integer_state_1()
    else:
        return (False, None)

def integer_state_1():
    global int_value
    ch = next_char()
    if nonzerodigit(ch):
        return (False, None)
    elif ch == END:
        return (True, int_value)
    elif digit(ch):
        return integer_state_1()
    else:
        return (False, None)

def integer_state_2():
    global int_value
    ch = next_char()
    if digit(ch):
        int_value*=10
        int_value+=int(ch)
        return integer_state_2()
    elif ch == END:
        return (True, int_value)
    else:
        return (False, None)

############
# Question 7 : pointfloat avec calcul de la valeur

def pointfloat():
    global int_value
    global exp_value
    init_char()
    int_value = 0
    exp_value = 0
    return pointfloat_state_0()

def pointfloat_state_0():
    global int_value
    global exp_value
    ch=next_char()
    if digit(ch):
        int_value+=int(ch)
        return pointfloat_state_2()
    elif ch == '.':
        return pointfloat_state_1()
    else:
        return (False, None)


def pointfloat_state_1():
    global int_value
    global exp_value
    ch=next_char()
    if digit(ch):
        int_value*=10
        int_value+=int(ch)
        exp_value+=1
        return pointfloat_state_3()
    else:
        return (False, None)

def pointfloat_state_2():
    global int_value
    global exp_value
    ch=next_char()
    if digit(ch):
        int_value*=10
        int_value+=int(ch)
        return pointfloat_state_2()
    elif ch == '.':
        return pointfloat_state_3()
    else:
        return (False, None)

def pointfloat_state_3():
    global int_value
    global exp_value
    ch=next_char()
    if digit(ch):
        exp_value+=1
        int_value*=10
        int_value+=int(ch)
        return pointfloat_state_3()
    if ch == END:
        return (True, int_value*10**-exp_value)
    else:
        return (False, None)


############
# Question 8 : exponent, exponentfloat et number

# La valeur du signe de l'exposant : 1 si +, -1 si -
sign_value = 0

def exponent():
    global exp_value
    global sign_value
    exp_value = 0
    sign_value = 0
    return exponent_stateA()

def exponent_stateA():
    global exp_value
    global sign_value
    ch=next_char()
    if ch == 'e' or ch == 'E':
        return exponent_stateB()
    return False, None

def exponent_stateB():
    global exp_value
    global sign_value
    ch=next_char()
    if digit(ch):
        exp_value+=int(ch)
        sign_value=1
        return exponent_stateD()
    elif ch == '+' or ch == '-':
        sign_value = 1 if ch == '+' else -1
        return exponent_stateC()
    return False, None

def exponent_stateC():
    global exp_value
    global sign_value
    ch=next_char()
    if digit(ch):
        exp_value+=int(ch)
        return exponent_stateD()
    return False, None

def exponent_stateD():
    global exp_value
    global sign_value
    ch=next_char()
    if digit(ch):
        exp_value*=10
        exp_value+=int(ch)
        return exponent_stateD()
    elif ch == END:
        return True, sign_value*exp_value
    return False, None

"""
    Exponentfloat
"""

def exponentfloat():
    global exp_value
    global sign_value
    global int_value
    exp_value = sign_value = int_value = 0
    return exponentfloat_state_A()

def exponentfloat_state_A():
    global int_value
    global exp_value
    ch=next_char()
    if digit(ch):
        int_value+=int(ch)
        return exponentfloat_state_D()
    elif ch == '.':
        return exponentfloat_state_B()
    else:
        return (False, None)


def exponentfloat_state_B():
    global int_value
    global exp_value
    ch=next_char()
    if digit(ch):
        int_value*=10
        int_value+=int(ch)
        exp_value+=-1
        return exponentfloat_state_C()
    else:
        return (False, None)

def exponentfloat_state_D():
    global int_value
    global exp_value
    ch=next_char()
    if digit(ch):
        int_value*=10
        int_value+=int(ch)
        return exponentfloat_state_D()
    elif ch == '.':
        return exponentfloat_state_C()
    elif ch == 'E' or ch == 'e':
        return exponentfloat_state_E()
    else:
        return (False, None)

def exponentfloat_state_C():
    global int_value
    global exp_value
    ch=next_char()
    if digit(ch):
        exp_value+=-1
        int_value*=10
        int_value+=int(ch)
        return exponentfloat_state_C()
    if ch == 'e' or ch == 'E':
        return exponentfloat_state_E()
    else:
        return (False, None)

def exponentfloat_state_E():
    global exp_value
    global sign_value
    global int_value
    int_value*=10**exp_value
    exp_value = 0
    ch=next_char()
    if digit(ch):
        sign_value=1
        exp_value+=sign_value*int(ch)
        return exponentfloat_state_G()
    elif ch == '+' or ch == '-':
        sign_value = 1 if ch == '+' else -1
        return exponentfloat_state_F()
    return False, None

def exponentfloat_state_F():
    global exp_value
    global sign_value
    ch=next_char()
    if digit(ch):
        exp_value+=sign_value*int(ch)
        return exponentfloat_state_G()
    return False, None

def exponentfloat_state_G():
    global exp_value
    global sign_value
    global int_value
    ch=next_char()
    if digit(ch):
        exp_value*=10
        exp_value+=sign_value*int(ch)
        return exponentfloat_state_G()
    elif ch == END:
        return True, int_value*10**exp_value
    return False,None

def number():
    global exp_value
    global sign_value
    global int_value
    exp_value = sign_value = int_value = 0
    return number_state_0()

def number_state_0():
    global exp_value
    global sign_value
    global int_value
    ch = next_char()
    if ch == '0':
        return number_state_1()
    elif ch == '.':
        return number_state_3()
    elif nonzerodigit(ch):
        int_value = int(ch)
        return number_state_2()
    return False, None

def number_state_1():
    global exp_value
    global sign_value
    global int_value
    ch = next_char()
    if ch == '0':
        return number_state_1()
    elif nonzerodigit(ch):
        int_value+=int(ch)
        return number_state_5()
    elif ch == '.':
        return number_state_4()
    elif ch == "E" or ch == 'e':
        return number_state_6()
    elif ch == END or ch == " ":
        return True, int_value
    return False, None

def number_state_2():
    global exp_value
    global sign_value
    global int_value
    ch = next_char()
    if ch == 'E' or ch == 'e':
        return number_state_6()
    elif digit(ch):
        int_value*=10
        int_value+=int(ch)
        return number_state_2()
    elif ch == '.':
        return number_state_4()
    elif ch == END or ch == " ":
        return True, int_value
    return False, None

def number_state_3():
    global exp_value
    global sign_value
    global int_value
    ch = next_char()
    if digit(ch):
        int_value+=int(ch)
        exp_value-=1
        return number_state_4()
    return False, None

def number_state_4():
    global exp_value
    global sign_value
    global int_value
    ch = next_char()
    if digit(ch):
        int_value*=10
        int_value+=int(ch)
        exp_value-=1
        return number_state_4()
    elif ch == 'E' or ch == 'e':
        return number_state_6()
    elif ch == END or ch == " ":
        return True, int_value*10**exp_value
    return False, None

def number_state_5():
    global exp_value
    global sign_value
    global int_value
    ch = next_char()
    if digit(ch):
        int_value*=10
        int_value+=int(ch)
        return number_state_5()
    elif ch == '.':
        return number_state_4()
    elif ch == 'E' or ch == 'e':
        return number_state_6()
    return False, None

def number_state_6():
    global exp_value
    global sign_value
    global int_value
    ch = next_char()
    int_value*=10**exp_value
    exp_value=0
    if ch == '+' or ch == '-':
        sign_value= 1 if ch == '+' else -1
        return number_state_7()
    elif digit(ch):
        sign_value=1
        exp_value=int(ch)
        return number_state_8()
    return False, None

def number_state_7():
    global exp_value
    global sign_value
    global int_value
    ch = next_char()
    if digit(ch):
        exp_value+=int(ch)
        return number_state_8()
    return False, None

def number_state_8():
    global exp_value
    global sign_value
    global int_value
    ch = next_char()
    if digit(ch):
        exp_value*=10
        exp_value+=int(ch)
        return number_state_8()
    elif ch == END or ch == " ":
        return True, int_value*10**(sign_value*exp_value)
    return False, None



########################
#####    Projet    #####
########################


V = set(('.', 'e', 'E', '+', '-', '*', '/', '(', ')', ' ')
        + tuple(str(i) for i in range(10)))


############
# Question 10 : eval_exp

def eval_exp():
    ch = next_char()
    if ch == '+':
        n1 = eval_exp()
        n2 = eval_exp()
        return n1 + n2
    elif ch == '-':
        n1 = eval_exp()
        n2 = eval_exp()
        return n1-n2
    elif ch == '*':
        n1 = eval_exp()
        n2 = eval_exp()
        return n1*n2
    elif ch == '/':
        n1 = eval_exp()
        n2 = eval_exp()
        return n1/n2
    elif ch == " ":
        return eval_exp()
    v = number()
    if v[0]:
        return v[1]
    else:
        raise Error


############
# Question 12 : eval_exp corrigé

current_char = ''

# Accès au caractère suivant de l'entrée sans avancer
def peek_char():
    global current_char
    if current_char == '':
        current_char = INPUT_STREAM.read(1)
    ch = current_char
    # print("@", repr(ch))
    if ch in V or ch in END:
        return ch
    

def consume_char():
    global current_char
    current_char = ''


def number_v2():
    global exp_value
    global sign_value
    global int_value
    exp_value = sign_value = int_value = 0
    return number_v2_state_0()

def number_v2_state_0():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    consume_char()
    if ch == '0':
        return number_v2_state_1()
    elif ch == '.':
        return number_v2_state_3()
    elif nonzerodigit(ch):
        int_value = int(ch)
        return number_v2_state_2()
    return False, None

def number_v2_state_1():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    consume_char()
    if ch == '0':
        return number_v2_state_1()
    elif nonzerodigit(ch):
        int_value+=int(ch)
        return number_v2_state_5()
    elif ch == '.':
        return number_v2_state_4()
    elif ch == "E" or ch == 'e':
        return number_v2_state_6()
    elif ch == END or ch == " ":
        return True, int_value
    return False, None

def number_v2_state_2():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    consume_char()
    if ch == 'E' or ch == 'e':
        return number_v2_state_6()
    elif digit(ch):
        int_value*=10
        int_value+=int(ch)
        return number_v2_state_2()
    elif ch == '.':
        return number_v2_state_4()
    elif ch == END or ch == " ":
        return True, int_value
    return False, None

def number_v2_state_3():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    consume_char()
    if digit(ch):
        int_value+=int(ch)
        exp_value-=1
        return number_v2_state_4()
    return False, None

def number_v2_state_4():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    consume_char()
    if digit(ch):
        int_value*=10
        int_value+=int(ch)
        exp_value-=1
        return number_v2_state_4()
    elif ch == 'E' or ch == 'e':
        return number_v2_state_6()
    elif ch == END or ch == " ":
        return True, int_value*10**exp_value
    return False, None

def number_v2_state_5():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    consume_char()
    if digit(ch):
        int_value*=10
        int_value+=int(ch)
        return number_v2_state_5()
    elif ch == '.':
        return number_v2_state_4()
    elif ch == 'E' or ch == 'e':
        return number_v2_state_6()
    return False, None

def number_v2_state_6():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    consume_char()
    int_value*=10**exp_value
    exp_value=0
    if ch == '+' or ch == '-':
        sign_value= 1 if ch == '+' else -1
        return number_v2_state_7()
    elif digit(ch):
        sign_value=1
        exp_value=int(ch)
        return number_v2_state_8()
    return False, None

def number_v2_state_7():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    consume_char()
    if digit(ch):
        exp_value+=int(ch)
        return number_v2_state_8()
    return False, None

def number_v2_state_8():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    consume_char()
    if digit(ch):
        exp_value*=10
        exp_value+=int(ch)
        return number_v2_state_8()
    elif ch == END or ch == " ":
        return True, int_value*10**(sign_value*exp_value)
    return False, None


def eval_exp_v2():
    ch = peek_char()
    if ch == '+':
        consume_char()
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        return n1 + n2
    elif ch == '-':
        consume_char()
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        return n1-n2
    elif ch == '*':
        consume_char()
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        return n1*n2
    elif ch == '/':
        consume_char()
        n1 = eval_exp_v2()
        n2 = eval_exp_v2()
        return n1/n2
    elif ch == " ":
        consume_char()
        return eval_exp_v2()
    v = number_v2()
    if v[0]:
        return v[1]
    else:
        raise Error


############
# Question 14 : automate pour Lex

operator = set(['+', '-', '*', '/'])

def LA_Lex():
    global exp_value
    global sign_value
    global int_value
    exp_value = sign_value = int_value = 0
    return LA_Lex_state_0()

def LA_Lex_state_0():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    consume_char()
    if ch == '0':
        return LA_Lex_state_1()
    elif ch == '.':
        return LA_Lex_state_3()
    elif nonzerodigit(ch):
        int_value = int(ch)
        return LA_Lex_state_2()
    elif ch == "(" or ch == ")" or ch in operator:
        return LA_Lex_state_9()
    return False, None

def LA_Lex_state_1():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    consume_char()
    if ch == '0':
        return LA_Lex_state_1()
    elif nonzerodigit(ch):
        int_value+=int(ch)
        return LA_Lex_state_5()
    elif ch == '.':
        return LA_Lex_state_4()
    elif ch == "E" or ch == 'e':
        return LA_Lex_state_6()
    elif ch == END:
        return True, int_value
    return False, None

def LA_Lex_state_2():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    consume_char()
    if ch == 'E' or ch == 'e':
        return LA_Lex_state_6()
    elif digit(ch):
        int_value*=10
        int_value+=int(ch)
        return LA_Lex_state_2()
    elif ch == '.':
        return LA_Lex_state_4()
    elif ch == END or ch == " ":
        return True, int_value
    return False, None

def LA_Lex_state_3():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    consume_char()
    if digit(ch):
        int_value+=int(ch)
        exp_value-=1
        return LA_Lex_state_4()
    return False, None

def LA_Lex_state_4():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    consume_char()
    if digit(ch):
        int_value*=10
        int_value+=int(ch)
        exp_value-=1
        return LA_Lex_state_4()
    elif ch == 'E' or ch == 'e':
        return LA_Lex_state_6()
    elif ch == END:
        return True, int_value*10**exp_value
    return False, None

def LA_Lex_state_5():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    consume_char()
    if digit(ch):
        int_value*=10
        int_value+=int(ch)
        return LA_Lex_state_5()
    elif ch == '.':
        return LA_Lex_state_4()
    elif ch == 'E' or ch == 'e':
        return LA_Lex_state_6()
    return False, None

def LA_Lex_state_6():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    consume_char()
    int_value*=10**exp_value
    exp_value=0
    if ch == '+' or ch == '-':
        sign_value= 1 if ch == '+' else -1
        return LA_Lex_state_7()
    elif digit(ch):
        sign_value=1
        exp_value=int(ch)
        return LA_Lex_state_8()
    return False, None

def LA_Lex_state_7():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    consume_char()
    if digit(ch):
        exp_value+=int(ch)
        return LA_Lex_state_8()
    return False, None

def LA_Lex_state_8():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    consume_char()
    if digit(ch):
        exp_value*=10
        exp_value+=int(ch)
        return LA_Lex_state_8()
    elif ch == END:
        return True, int_value*10**(sign_value*exp_value)
    return False, None

def LA_Lex_state_9():
    ch = peek_char()
    consume_char()
    if ch == END:
        return True, None
    return False, None

############
# Question 15 : automate pour Lex avec token

# Token
NUM, ADD, SOUS, MUL, DIV, OPAR, FPAR = range(7)
token_value = 0



def FA_Lex_w_token():
    global exp_value
    global sign_value
    global int_value
    exp_value = sign_value = int_value = 0
    return FA_Lex_w_token_state_0()

def FA_Lex_w_token_state_0():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    consume_char()
    if ch == '0':
        return FA_Lex_w_token_state_1()
    elif ch == '.':
        return FA_Lex_w_token_state_3()
    elif nonzerodigit(ch):
        int_value = int(ch)
        return FA_Lex_w_token_state_2()
    elif ch == "(":
        int_value = OPAR
        return FA_Lex_w_token_state_9()
    elif ch == ")":
        int_value = FPAR
        return FA_Lex_w_token_state_9()
    elif ch == "*":
        int_value = MUL
        return FA_Lex_w_token_state_9()
    elif ch == "/":
        int_value = DIV
        return FA_Lex_w_token_state_9()
    elif ch == "+":
        int_value = ADD
        return FA_Lex_w_token_state_9()
    elif ch == "-":
        int_value = SOUS
        return FA_Lex_w_token_state_9()
    elif ch == " ":
        return FA_Lex_w_token_state_0()
    return False, None

def FA_Lex_w_token_state_1():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    if ch == '0':
        consume_char()
        return FA_Lex_w_token_state_1()
    elif nonzerodigit(ch):
        consume_char()
        int_value+=int(ch)
        return FA_Lex_w_token_state_5()
    elif ch == '.':
        consume_char()
        return FA_Lex_w_token_state_4()
    elif ch == "E" or ch == 'e':
        consume_char()
        return FA_Lex_w_token_state_6()
    return True, NUM

def FA_Lex_w_token_state_2():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    if ch == 'E' or ch == 'e':
        consume_char()
        return FA_Lex_w_token_state_6()
    elif digit(ch):
        consume_char()
        int_value*=10
        int_value+=int(ch)
        return FA_Lex_w_token_state_2()
    elif ch == '.':
        consume_char()
        return FA_Lex_w_token_state_4()
    return True, NUM

def FA_Lex_w_token_state_3():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    consume_char()
    if digit(ch):
        int_value+=int(ch)
        exp_value-=1
        return FA_Lex_w_token_state_4()
    return False, None

def FA_Lex_w_token_state_4():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    if digit(ch):
        consume_char()
        int_value*=10
        int_value+=int(ch)
        exp_value-=1
        return FA_Lex_w_token_state_4()
    elif ch == 'E' or ch == 'e':
        consume_char()
        return FA_Lex_w_token_state_6()
    return True, NUM

def FA_Lex_w_token_state_5():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    consume_char()
    if digit(ch):
        int_value*=10
        int_value+=int(ch)
        return FA_Lex_w_token_state_5()
    elif ch == '.':
        return FA_Lex_w_token_state_4()
    elif ch == 'E' or ch == 'e':
        return FA_Lex_w_token_state_6()
    return False, None

def FA_Lex_w_token_state_6():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    consume_char()
    int_value*=10**exp_value
    exp_value=0
    if ch == '+' or ch == '-':
        sign_value= 1 if ch == '+' else -1
        return FA_Lex_w_token_state_7()
    elif digit(ch):
        sign_value=1
        exp_value=int(ch)
        return FA_Lex_w_token_state_8()
    return False, None

def FA_Lex_w_token_state_7():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    consume_char()
    if digit(ch):
        exp_value+=int(ch)
        return FA_Lex_w_token_state_8()
    return False, None

def FA_Lex_w_token_state_8():
    global exp_value
    global sign_value
    global int_value
    ch = peek_char()
    if digit(ch):
        consume_char()
        exp_value*=10
        exp_value+=int(ch)
        return FA_Lex_w_token_state_8()
    return True, NUM

def FA_Lex_w_token_state_9():
    global int_value
    return True, int_value



# Fonction de test
if __name__ == "__main__":
    print("@ Test interactif de l'automate")
    print("@ Vous pouvez changer l'automate testé en modifiant la fonction appelée à la ligne 'ok = ... '.")
    print("@ Tapez une entrée:")
    try:
        ok = integer_Q2() # changer ici pour tester un autre automate sans valeur
        # ok, val = integer() # changer ici pour tester un autre automate avec valeur
        # ok, val = True, eval_exp() # changer ici pour tester eval_exp et eval_exp_v2
        if ok:
            print("Accepted!")
            # print("value:", val) # décommenter ici pour afficher la valeur (question 4 et +)
        else:
            print("Rejected!")
            # print("value so far:", int_value) # décommenter ici pour afficher la valeur en cas de rejet
    except Error as e:
        print("Error:", e)
