class Cursor:
    def __init__(self,script):
        self.script = script
        self.index = 0
        self.row = 1
        self.column = 1

    def __str__(self):
        return f"Cursor: index:{self.index} row:{self.row} column:{self.column} value:{self.script[self.index] if not self.eof() else 'None'}"

    def __repr__(self):
        return str(self)

    def eof(self):
        return self.index == len(self.script)

    def skip(self, chars):
        while not self.eof() and self.get_char() in chars:
            self.advance()

    def skip_spaces(self):
        while not self.eof() and self.get_char() in ' \t\r\n':
            self.advance()

    def skip_char_ifexpected(self, char):
        if self.get_char() in char:
            self.advance()
            return True

        return False

    def skip_char_ifexpected_anyof(self, char):
        if self.get_char() in char:
            ch = self.get_char()
            self.advance()
            return True, ch

        return False, None

    def peek_next_nonspace(self):
        temp_index = self.index
        while self.script[temp_index] in ' \t\n':
            temp_index += 1

        return self.script[temp_index]

    def peek_next_nonspace_any(self, character):
        temp_index = self.index
        while self.script[temp_index] in ' \t\n':
            temp_index += 1

        return self.script[temp_index] in character

    def get_char(self):
        return self.script[self.index]

    def char_is(self, char):
        return True if self.get_char() == char else False

    def char_isnot(self, char):
        return False if self.get_char() == char else True

    def char_is_digit(self):
        return True if self.get_char().isdigit() else False

    def advance(self):
        if not self.eof():
            if self.script[self.index] == '\n':
                self.index += 1
                self.column = 1
                self.row += 1
            else:
                self.index += 1
                self.column += 1


    # def get_index_first(self, character):
    #     i = self.index
    #     while self.script[i] != character:
    #         i += 1
    #     return i

    def is_nextchar_expected(self, character):

        while self.get_char()  in ' \r\n\t':
            self.advance()
        return True if self.get_char() == character else False