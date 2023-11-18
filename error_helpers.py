class emsg:
    def __init__(self, msg, information=''):
        self.message = msg
        self.information = information

    def __str__(self):
        return f"error message: {self.message}. " + (f"[more information : {self.information}]" if len(self.information) > 0 else '')

    def __repr__(self):
        return str(self)


def parsing_error(cursor, msg):
    print(f"{cursor} : {str(msg) if msg is not None else ''}")
    exit(1)

