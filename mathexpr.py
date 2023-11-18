from strtypes import *


class Stack:
    def __init__(self):
        self.data = []

    def push(self, data):
        self.data.append(data)

    def pop(self):
        return self.data.pop()

    def top(self):
        return self.data[-1]

    def is_empty(self):
        return len(self.data) == 0

def precedence(ch):
    if ch in '^':
        return 3
    elif ch in '*/':
        return 2
    elif ch in '+-':
        return 1
    else:
        return -1




def postfix(inotation):

    index = 0
    expstack = Stack()
    result = []

    while index < len(inotation):
        while index < len(inotation) and is_whitespace(inotation[index]):
            index += 1
        operand = ''

        #if is_operand(inotation[index]):
        if is_operand(inotation[index]):
            while index < len(inotation) and is_operand(inotation[index]):
                operand += inotation[index]
                index += 1
            if operand != '':
                result.append(operand)

        elif inotation[index] == '(':
            expstack.push(inotation[index])
            index += 1
        elif inotation[index] == ')':

            while expstack.top() != '(':
                result.append(expstack.pop())
            expstack.pop()
            index += 1
        elif is_operator(inotation[index]):
            while not expstack.is_empty() and precedence(inotation[index]) <= precedence(expstack.top()):
                result.append(expstack.pop())
            expstack.push(inotation[index])
            index += 1

    while not expstack.is_empty():
        result.append(expstack.pop())

    return result

def prefix(infix):
    infix = infix[::-1]

    temp = list(infix)
    for i, ch in enumerate(temp):
        if ch == '(':
            temp[i] = ')'
        if ch == ')':
            temp[i] = '('

    infix  = ''.join(temp)

    infix = postfix(infix)
    infix.reverse()

    return infix

def eval_math(x, y, op):
    if op == '+':
        return x + y
    elif op == '-':
        return x - y
    elif op == '*':
        return x * y
    elif op == '/':
        return x / y
    elif op == '^':
        return x ** y

def eval_postfix(notation):
    result = []
    index = 0
    while index < len(notation):

        if is_operand(notation[index]):
            result.append(notation[index])
            index += 1

        elif notation[index] in '+-*/^':
            y = str(result.pop())
            x = str(result.pop())

            y = cast_to(y, detect_type(y))
            x = cast_to(x, detect_type(x))

            result.append(eval_math(x, y, notation[index]))
            index += 1
        else:
            index += 1

    return result[0]


if __name__ == '__main__':

    print(' '.join(postfix('1 * (2 + 3)')))
    print(eval_postfix(postfix('1 * (2 + 3)')))
    print(''.join(prefix('1 * (2 + 3)')))