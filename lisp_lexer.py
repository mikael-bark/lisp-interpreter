import sys
import itertools
from lisp_tokens import Tokens

class Lexer:
    def __init__(self, input_iter):
        self.input_iter = input_iter
        self.lookahead_char = None
        self.filter_set = set()
        self.state_map = {}
        self.filter_set.add(Tokens.ws)
        self.row_ind = 0
        self.col_ind = 0

    class State:
        def __init__(self, transition_map, accept_token):
            self.transition_map = transition_map
            self.accept_token = accept_token

    def next_token(self, start_state):
        def next_state(state, string_buffer):
            assert self.lookahead_char in state.transition_map
            if self.lookahead_char == '\n':
                self.row_ind += 1
                self.col_ind = 0
            elif self.lookahead_char == '\n':
                self.col_ind += 1
            string_buffer += self.lookahead_char
            new_state_id = state.transition_map[self.lookahead_char]
            state = lexer.state_map[new_state_id]
            return state, string_buffer
        string_buffer = ""
        if self.lookahead_char == None:
            self.lookahead_char = next(self.input_iter)
        state, string_buffer = next_state(start_state, string_buffer)
        for self.lookahead_char in self.input_iter:
            if self.lookahead_char in state.transition_map:
                state, string_buffer = next_state(state, string_buffer)
            else:
                break
        if state.accept_token and state != start_state:
            if state.accept_token in self.filter_set:
                return self.next_token(start_state)
            else:
                assert state.accept_token
                return state.accept_token(string_buffer)
        elif state.accept_token == None:
            print(" " * 4, "Error: lexer got unexpected character: ", ord(self.lookahead_char),
                  " on row: ", self.row_ind,
                  " column: ", self.col_ind, sep = '')
            assert False
            return None
        else:
            assert False # Something is really wrong

lexer = Lexer(
    itertools.chain(
        iter(sys.stdin.read()),
        iter('\0')))

lexer.state_map[1] = Lexer.State(
    transition_map = dict(
        itertools.chain(
            itertools.product("0123456789", [2]))),
    accept_token = None
)

lexer.state_map[2] = Lexer.State(
    transition_map = dict(
        itertools.chain(
            itertools.product("0123456789", [2]))),
    accept_token = Tokens.float
)

lexer.state_map[3] = Lexer.State(
    transition_map = dict(
        itertools.chain(
            itertools.product("ft", [9]))),
    accept_token = None
)

lexer.state_map[4] = Lexer.State(
    transition_map = dict(
        itertools.chain(
            itertools.product("\n %0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"\
                              "abcdefghijklmnopqrstuvwxyz~", [5]))),
    accept_token = None
)

lexer.state_map[5] = Lexer.State(
    transition_map = dict(
        itertools.chain(
            itertools.product("\n %0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"\
                              "abcdefghijklmnopqrstuvwxyz~", [5]))),
    accept_token = Tokens.string
)

lexer.state_map[6] = Lexer.State(
    transition_map = dict(
        itertools.chain(
            itertools.product("-0123456789?ABCDEFGHIJKLMNOPQRSTUVWXYZ_a"\
                              "bcdefghijklmnopqrstuvwxyz", [6]))),
    accept_token = Tokens.identifier
)

lexer.state_map[7] = Lexer.State(
    transition_map = dict(
        itertools.chain(
            itertools.product("\n ", [8]))),
    accept_token = None
)

lexer.state_map[8] = Lexer.State(
    transition_map = dict(
        itertools.chain(
            itertools.product("\n ", [8]))),
    accept_token = Tokens.ws
)

lexer.state_map[9] = Lexer.State(
    transition_map = {},
    accept_token = Tokens.boolean
)

lexer.state_map[10] = Lexer.State(
    transition_map = {},
    accept_token = Tokens.operator
)

lexer.state_map[11] = Lexer.State(
    transition_map = {},
    accept_token = Tokens.CHAR
)

lexer.state_map[12] = Lexer.State(
    transition_map = {},
    accept_token = Tokens.CHAR
)

lexer.state_map[13] = Lexer.State(
    transition_map = dict(
        itertools.chain(
            itertools.product(".", [1]),
            itertools.product("0123456789", [13]))),
    accept_token = Tokens.integer
)

lexer.state_map[14] = Lexer.State(
    transition_map = dict(
        itertools.chain(
            itertools.product("0123456789", [13]))),
    accept_token = Tokens.operator
)

lexer.state_map[15] = Lexer.State(
    transition_map = dict(
        itertools.chain(
            itertools.product("\n ", [8]),
            itertools.product("\"'(", [12]),
            itertools.product("#", [3]),
            itertools.product("*+<=>", [10]),
            itertools.product("-", [14]),
            itertools.product("0123456789", [13]),
            itertools.product("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmn"\
                              "opqrstuvwxyz", [6]))),
    accept_token = None
)

lexer.state_map[16] = Lexer.State(
    transition_map = dict(
        itertools.chain(
            itertools.product("\0", [11]),
            itertools.product("\n ", [8]))),
    accept_token = None
)

lexer.state_map[17] = Lexer.State(
    transition_map = dict(
        itertools.chain(
            itertools.product("\0", [11]),
            itertools.product("\n ", [8]),
            itertools.product("\"'()", [12]),
            itertools.product("#", [3]),
            itertools.product("*+<=>", [10]),
            itertools.product("-", [14]),
            itertools.product("0123456789", [13]),
            itertools.product("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmn"\
                              "opqrstuvwxyz", [6]))),
    accept_token = None
)

lexer.state_map[18] = Lexer.State(
    transition_map = dict(
        itertools.chain(
            itertools.product("\0", [11]),
            itertools.product("\n ", [8]),
            itertools.product(")", [12]))),
    accept_token = None
)

lexer.state_map[19] = Lexer.State(
    transition_map = dict(
        itertools.chain(
            itertools.product("\n ", [8]),
            itertools.product(")", [12]))),
    accept_token = None
)

lexer.state_map[20] = Lexer.State(
    transition_map = dict(
        itertools.chain(
            itertools.product("\n ", [8]),
            itertools.product("\"", [12]))),
    accept_token = None
)

lexer.state_map[21] = Lexer.State(
    transition_map = dict(
        itertools.chain(
            itertools.product("\n ", [8]),
            itertools.product("\"(", [12]),
            itertools.product("#", [3]),
            itertools.product("*+<=>", [10]),
            itertools.product("-", [14]),
            itertools.product("0123456789", [13]),
            itertools.product("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmn"\
                              "opqrstuvwxyz", [6]))),
    accept_token = None
)

