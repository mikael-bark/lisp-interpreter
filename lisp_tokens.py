
class Token:
    def __init__(self, text, type_str):
        self.text = text
        self.type_str = type_str

    def __getattr__(self, name):
        if name == "value":
            if type(self) == Tokens.CHAR:
                return self.text
            else:
                return type(self)

class Tokens:
    class integer(Token):
        def __init__(self, text):
            super().__init__(text, "integer")

    class float(Token):
        def __init__(self, text):
            super().__init__(text, "float")

    class boolean(Token):
        def __init__(self, text):
            super().__init__(text, "boolean")

    class string(Token):
        def __init__(self, text):
            super().__init__(text, "string")

    class identifier(Token):
        def __init__(self, text):
            super().__init__(text, "identifier")

    class operator(Token):
        def __init__(self, text):
            super().__init__(text, "operator")

    class ws(Token):
        def __init__(self, text):
            super().__init__(text, "ws")

    class CHAR(Token):
        def __init__(self, text):
            super().__init__(text, "CHAR")
