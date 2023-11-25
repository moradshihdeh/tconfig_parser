from error_helpers import *

def detect_type(value):
    dot = 0
    index = 0
    if value[index] == '-':
        index += 1
    while index < len(value) and (is_chdigit(value[index]) or is_chdot(value[index])):
        if is_chdot(value[index]):
            dot += 1
        index += 1

    if index >= len(value):
        if dot == 1:
            return 'float'
        elif dot == 0:
            return 'int'

    return 'string'

def cast_to(value, type):
    if type == 'int':
        return int(value)
    elif type == 'float':
        return float(value)
    else:
        return str(value)

def is_underscore(character):
    return character == '_'

def is_alpha(character):
    return character.isalpha()

def is_chdigit(character):
    return character.isdigit()

def is_chnumber(character):
    return character.isdigit() or character =='.'

def is_chdot(character):
    return character == '.'

def is_space(character):
    return character in ' \t\n'

def is_whitespace(character):
    return character in ' \t\n'
def is_valid_name_char(character):
    return is_alpha(character) or is_chdigit(character) or is_underscore(character)

def is_parenthesis(character):
    return character in '()'

def is_math_symbol(character):
    return character in '+-=*/^%'

def is_operator(character):
    return character in '+-=*/^'

def is_choperand(character):
    return is_chdigit(character) or is_chdot(character)

def is_operand(value):
    operand = True
    for ch in value:
        if not is_choperand(ch):
            operand = False
    return operand

def is_math_special(character):
    return character in '\\'
def is_comment_symbol(character):
    return character == '#'

def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def is_valid_chpath(character):
    return character.isalpha() or character.isdigit() or character in './\\_()-'

if __name__ == '__main__':
    print(detect_type('1.99a9..'))