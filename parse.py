
from cursor import Cursor
from strtypes import *
from mathexpr import *
from error_helpers import *

global_sight = {}

RESERVED = ['namespace', 'list', 'struct', 'string', 'float', 'int']
MATH_FUNCTIONS = ['cos', 'tan', 'sin',
                  'tanh', 'asin', 'acos',
                  'atan', 'atanh', 'ceil',
                  'floor']

def skip_line_comment(cursor):

    while cursor.get_char() != '\n':
        cursor.advance()
    return cursor

def scan_next_reserved(cursor):

    token = ''
    cursor.skip('\n \t')

    if cursor.get_char() == '#':
        return '#', cursor

    if not is_alpha(cursor.get_char()):
        parsing_error(cursor,emsg('errors parsing comments'))
    while is_alpha(cursor.get_char()) or is_chdigit(cursor.get_char()):
        token += cursor.get_char()
        cursor.advance()


    return token, cursor

def scan_next_valid_name(cursor):

    token = ''
    cursor.skip_spaces()

    if cursor.get_char() == '#':
        return '#', cursor

    if cursor.get_char() in '0123456789.':
        parsing_error(cursor, emsg('error parsing next valid name cant start with numbers', ))

    while is_valid_name_char(cursor.get_char()):
        token += cursor.get_char()
        cursor.advance()

    return token, cursor


def scan_next_int(cursor):

    number = ''
    cursor.skip_spaces()
    if cursor.get_char() == '-':
        number += cursor.get_char()
        cursor.advance()

    if not is_chdigit(cursor.get_char()):
        parsing_error(cursor, emsg(f"Invalid number expected integer"))

    while is_chdigit(cursor.get_char()):
        number += cursor.get_char()
        cursor.advance()

    cursor.skip_spaces()
    return int(number), cursor

def scan_next_float(cursor):
    number = ''
    cursor.skip('\n \t')
    dots = 0

    if cursor.skip_char_ifexpected('-'):
        number += '-'

    while is_chdigit(cursor.get_char()) or cursor.get_char() == '.':
        if cursor.get_char() == '.':
            dots += 1
            if dots > 1:
                parsing_error(cursor, emsg('Invalid float format', 'check the dots'))
        number += cursor.get_char()
        cursor.advance()

    cursor.skip(' \t\n')
    print(cursor)
    print(number)
    return float(number), cursor

NUMBER = 'number'
SYMBOL = 'symbol'
SPACE = 'space'
SCANNING = 'scanning'
def solve_next_expr(cursor):
    expr = ''
    state = SCANNING
    expected = NUMBER
    has_unary = False

    # 100 + 100
    # number number number space symbol space number
    cursor.skip_spaces()
    while cursor.char_isnot(';') and cursor.char_isnot(',') and cursor.char_isnot(']'):

        if state == SCANNING:
            if (is_chnumber(cursor.get_char()) or cursor.get_char() in '-+') and expected == NUMBER:
                state = NUMBER
                expected = SYMBOL

                if cursor.get_char() in '-+':
                    expr += '(0'
                    expr += cursor.get_char()
                    cursor.advance()
                    has_unary = True
                while cursor.get_char().isdigit() or cursor.get_char() == '.':
                    expr += cursor.get_char()
                    cursor.advance()
                if has_unary:
                    expr += ')'
                    has_unary = False
                cursor.skip_spaces()
            elif not is_chdigit(cursor.get_char()):
                parsing_error(cursor, emsg('error parsing, expression format is incorrect'))

        elif is_chnumber(cursor.get_char()) and expected == NUMBER:
            state = NUMBER
            expected = SYMBOL
            while cursor.get_char().isdigit() or cursor.get_char() == '.':
                expr += cursor.get_char()
                cursor.advance()
            if has_unary:
                has_unary = False
                expr += ')'
            cursor.skip_spaces()

        elif is_operator(cursor.get_char()) and expected == SYMBOL:
            expr += cursor.get_char()
            cursor.advance()
            if cursor.peek_next_nonspace() in '+-':
                cursor.skip_spaces()
                has_unary = True
                expr += '(0'
                expr += cursor.get_char()

                cursor.advance()

            cursor.skip_spaces()
            expected = NUMBER

        else:
            parsing_error(cursor, emsg('math expression not formatted properly','check the format'))
    return eval_postfix(postfix(expr)), cursor

def scan_next_string(cursor):


    cursor.skip_spaces()
    error, quote_type = cursor.skip_char_ifexpected_anyof('\'\"')
    result = ''
    while cursor.char_isnot(';') and cursor.char_isnot(',') and cursor.char_isnot(']'):
        string = ''
        while cursor.get_char() != quote_type:
            string += cursor.get_char()
            cursor.advance()

        if cursor.skip_char_ifexpected(quote_type):
            cursor.skip_spaces()
            if cursor.skip_char_ifexpected('+'):
                cursor.skip_spaces()
                error, quote_type = cursor.skip_char_ifexpected_anyof('\'\"')
            elif cursor.skip_char_ifexpected('*'):
                cursor.skip_spaces()
                repeat, cursor = scan_next_int(cursor)
                string = string * repeat
                cursor.skip_spaces()
            elif cursor.peek_next_nonspace_any(';,]') == False:
                parsing_error(cursor,  emsg('error in string format', f"found {cursor.get_char()} expected any of: \'\"]"))
        result += string

            #if concatenation


    cursor.skip_spaces()

    return result, cursor

def is_valid_chvalue(chvalue):
    return is_alpha(chvalue) or is_chdigit(chvalue) or is_chdot(chvalue)

def scan_next_value(cursor):
    cursor.skip(' \t\n')
    value = ''
    if cursor.get_char() in "\"\'":
        return scan_next_string(cursor)
    while is_valid_chvalue(cursor.get_char()):
        value += cursor.get_char()
        cursor.advance()

    return value, cursor
def scan_next_struct(cursor):
    result = {}
    cursor.skip_spaces()
    cursor.skip_char_ifexpected('{')
    cursor.skip_spaces()

    while cursor.char_isnot('}'):
        cursor.skip_spaces()
        value = None
        id = None

        # scan for field id:
        if cursor.skip_char_ifexpected('.'):
            cursor.skip_spaces()
            id, cursor = scan_next_valid_name(cursor)
            cursor.skip_spaces()
            if not cursor.skip_char_ifexpected(':'):
                parsing_error(cursor, emsg('error parsing struct','expected : '))

            value, cursor = scan_next_value(cursor)
            value_type = detect_type(value)

            if value_type == 'int':
                value = int(value)
            elif value_type == 'string':
                value = value
            elif value_type == 'float':
                value = float(value)
            else:
                parsing_error(cursor, emsg(f"Unknown value type:{value_type}"))
        else:
            parsing_error(cursor, emsg('format error','expected a dot(.) before var'))

        result[str(id)] = value
        cursor.skip_spaces()
        cursor.skip_char_ifexpected(',')

    cursor.skip_char_ifexpected('}')
    cursor.skip_spaces()

    return result, cursor


def scan_next_list(cursor):

    #scan type of list
    list_type, cursor = scan_next_reserved(cursor)
    result = []
    cursor.skip_spaces()
    if cursor.skip_char_ifexpected('[') != True:
        parsing_error(cursor, emsg('list format error', 'expected ['))

    cursor.skip_spaces()
    while cursor.char_isnot(']'):
        cursor.skip_spaces()
        temp = ''
        if list_type == 'int':
            temp, cursor = solve_next_expr(cursor)
            temp_type = detect_type(str(temp))
            if temp_type != 'int':
                parsing_error(cursor, emsg(f"invalid value {temp}", f"expected int got {temp_type}"))
            temp = int(temp)
        elif list_type == 'string':
            temp, cursor = scan_next_string(cursor)
        elif list_type == 'float':
            temp, cursor = solve_next_expr(cursor)
            temp_type = detect_type(str(temp))
            if temp_type != 'float':
                parsing_error(cursor, emsg(f"invalid value {temp}", f"expected float got {temp_type}"))
            temp = float(temp)
        elif list_type == 'list':
            temp, cursor = scan_next_list(cursor)
        elif list_type == 'struct':
            temp, cursor = scan_next_struct(cursor)
        else:
            parsing_error(cursor,f"Unknown type : {list_type}")
        result.append(temp)
        cursor.skip_spaces()

        if cursor.skip_char_ifexpected(',') == False:
            if cursor.peek_next_nonspace() != ']':
                parsing_error(cursor,f"list error, incorrect items not formatted properly")

    cursor.skip_char_ifexpected(']')
    cursor.skip_spaces()
    return result, cursor


def scan_namespace_body(cursor, access_data, namespace):
    body = {}

    cursor.skip_spaces()
    if cursor.skip_char_ifexpected('{') != True:
        parsing_error(cursor,emsg(f" Format Error while scanning namespace:[{namespace}] elements",f"was expected {'{'} after {namespace} "))
    cursor.skip_spaces()

    while cursor.char_isnot('}'):
        var_type, cursor = scan_next_reserved(cursor)

        if var_type not in RESERVED:
            parsing_error(cursor, emsg(f"type:{var_type}",f"was expecting any of {RESERVED}"))

        var_name, cursor = scan_next_valid_name(cursor)

        if var_type != 'namespace':
            cursor.skip_spaces()
            if not cursor.skip_char_ifexpected('='):
                parsing_error(cursor, emsg(f"message parsing for = sign for variable type '{var_type}' variable name '{var_name}'",f"was expecting"))

        cursor.skip_spaces()
        if var_type == 'int':
            var_value, cursor = solve_next_expr(cursor)
            var_value = int(var_value)
            cursor.skip_char_ifexpected(';')
        elif var_type == 'float':

            var_value, cursor = solve_next_expr(cursor)
            var_value = float(var_value)
            cursor.skip_char_ifexpected(';')

        elif var_type == 'string':
            var_value, cursor = scan_next_string(cursor)
            if cursor.skip_char_ifexpected(';') == False:
                print(var_value)
                parsing_error(cursor, emsg(f"code format error",'expected ;'))
        elif var_type == 'list':
            var_value, cursor = scan_next_list(cursor)
        elif var_type == 'struct':
            var_value, cursor = scan_next_struct(cursor)
        elif var_type == 'namespace':
            var_value, cursor = scan_namespace_body(cursor, access_data, var_name)
            cursor.skip_spaces()
            cursor.skip_char_ifexpected('}')
            cursor.skip_spaces()
        else:
            parsing_error(cursor, emsg(f"Unknown variable type: {var_type}."))


        body[var_name] = var_value
        cursor.skip(' \n\t')


    return body, cursor




def parse(cursor):

    result = {}

    while not cursor.eof():
        cursor.skip_spaces()
        token, cursor = scan_next_reserved(cursor)
        if token == 'namespace':
            access_data = {}
            #scan for the name of the namespace
            current_namespace, cursor = scan_next_valid_name(cursor)

            result[current_namespace], cursor = scan_namespace_body(cursor, access_data, current_namespace)

            cursor.skip_char_ifexpected('}')

        elif is_comment_symbol(cursor.get_char()):
            cursor = skip_line_comment(cursor)
        else:
            if token != 'namespace':
                parsing_error(cursor, emsg(f"UnKnown type:{token}", "was expecting any of namespace"))

        cursor.skip('\n \t')
    return result

'''
isnumeric()
isalpha()
isspace()
isascii()
isalnum()
'''