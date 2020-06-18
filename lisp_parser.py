
from lisp_lexer import lexer
from itertools import chain
from lisp_tokens import Tokens
from helpers import iter_cdr, Node

class TreeNode(Node):
    def __init__(self, name = "", value = "", car = None, cdr = None):
        super().__init__(value, car, cdr)
        self.name = name
        self.value = value

class Parser:
    def __init__(self):
        self.state_map = {}
        self.callback_map = {}

    class State:
        def __init__(self, lexer_state, shift_map, reduce_map, goto_map):
            self.lexer_state = lexer_state
            self.shift_map = shift_map
            self.reduce_map = reduce_map
            self.goto_map = goto_map

    def parse(self):
        state_stack = []
        input_ind = 0
        state_id = 1
        state = self.state_map[state_id]
        state_stack = [state.goto_map]
        tree_node_stack = []
        node_stack = []
        char_count = 0
        terminal = lexer.next_token(state.lexer_state)
        goal_state = self.state_map[2]
        def shift(state, terminal, state_stack, node_stack):
            #input_ind += 1
            state_id = state.shift_map[terminal.value]
            print("parser: state_id", state_id)
            state = self.state_map[state_id]
            state_stack.append(
                state.goto_map)
            node_stack.append(
                TreeNode(
                    terminal.type_str,
                    terminal.text, None, None))
            assert state.lexer_state != None
            terminal = lexer.next_token(state.lexer_state)
            return state, terminal, state_stack, node_stack
        def reduce(state, terminal, state_stack, node_stack):
            name, num_children = state.reduce_map[terminal.value]
            assert len(state_stack) > num_children
            pop_count = num_children
            tree_node_list = None
            while pop_count > 0:
                tree_node = node_stack.pop()
                if tree_node.name != "CHAR":
                    if tree_node_list:
                        tree_node.cdr = tree_node_list
                        tree_node_list = tree_node
                    else:
                        tree_node_list = tree_node
                state_stack.pop()
                pop_count -= 1
            assert state_stack[-1]
            state_id = state_stack[-1][name]
            print("parser: state_id", state_id)
            state = self.state_map[state_id]
            state_stack.append(state.goto_map)
            char_count = 0
            if name == "atom":
                node_stack.append(TreeNode("atom", "", tree_node_list, None))
            elif name == "s_expr":
                new_node = TreeNode("s_expr", "", tree_node_list, None)
                node_stack.append(new_node)
                parser.callback_map[name](new_node)
            elif name == "qs_expr":
                node_stack.append(TreeNode("qs_expr", "", tree_node_list, None))
            elif name == "list":
                new_node = TreeNode("list", "", tree_node_list, None)
                node_stack.append(new_node)
                parser.callback_map[name](new_node)
            elif name == "program":
                new_node = TreeNode("program", "", tree_node_list, None)
                node_stack.append(new_node)
                parser.callback_map[name](new_node)
            return state, state_stack, node_stack
        while terminal.value != "\0" or state != goal_state:
            if terminal.value in state.reduce_map:
                state, state_stack, node_stack = reduce(state, terminal, state_stack, node_stack)
            elif terminal.value in state.shift_map:
                state, terminal, state_stack, node_stack = shift(state, terminal, state_stack, node_stack)
            else:
                if terminal.value == '\0':
                    print("Error: Unexpected end of input")
                else:
                    print("Error: Unexpected character '", terminal.value, "'", sep = '')
                return
        assert len(node_stack) == 1
        return node_stack[0]

parser = Parser()

parser.state_map[1] = Parser.State(
    lexer_state = lexer.state_map[15],
    shift_map = {
        Tokens.boolean : 9,
        Tokens.float : 9,
        Tokens.identifier : 9,
        Tokens.integer : 9,
        Tokens.operator : 9,
        "\"" : 10,
        "'" : 13,
        "(" : 15
    },
    reduce_map = {},
    goto_map = {
        "program" : 2,
        "list" : 3,
        "qs_expr" : 4,
        "s_expr" : 4,
        "atom" : 8
    }
)

parser.state_map[2] = Parser.State(
    lexer_state = lexer.state_map[7],
    shift_map = {},
    reduce_map = {},
    goto_map = {}
)

parser.state_map[3] = Parser.State(
    lexer_state = lexer.state_map[16],
    shift_map = {},
    reduce_map = {
        "\0" : ("program", 1)
    },
    goto_map = {}
)

parser.state_map[4] = Parser.State(
    lexer_state = lexer.state_map[17],
    shift_map = {
        Tokens.boolean : 9,
        Tokens.float : 9,
        Tokens.identifier : 9,
        Tokens.integer : 9,
        Tokens.operator : 9,
        "\"" : 10,
        "'" : 13,
        "(" : 15
    },
    reduce_map = {
        "\0" : ("list", 1),
        ")" : ("list", 1)
    },
    goto_map = {
        "list" : 5,
        "qs_expr" : 6,
        "s_expr" : 6,
        "atom" : 8
    }
)

parser.state_map[5] = Parser.State(
    lexer_state = lexer.state_map[18],
    shift_map = {},
    reduce_map = {
        "\0" : ("list", 2),
        ")" : ("list", 2)
    },
    goto_map = {}
)

parser.state_map[6] = Parser.State(
    lexer_state = lexer.state_map[17],
    shift_map = {
        Tokens.boolean : 9,
        Tokens.float : 9,
        Tokens.identifier : 9,
        Tokens.integer : 9,
        Tokens.operator : 9,
        "\"" : 10,
        "'" : 13,
        "(" : 15
    },
    reduce_map = {
        "\0" : ("list", 1),
        ")" : ("list", 1)
    },
    goto_map = {
        "list" : 7,
        "qs_expr" : 4,
        "s_expr" : 4,
        "atom" : 8
    }
)

parser.state_map[7] = Parser.State(
    lexer_state = lexer.state_map[18],
    shift_map = {},
    reduce_map = {
        "\0" : ("list", 2),
        ")" : ("list", 2)
    },
    goto_map = {}
)

parser.state_map[8] = Parser.State(
    lexer_state = lexer.state_map[17],
    shift_map = {},
    reduce_map = {
        Tokens.identifier : ("s_expr", 1),
        Tokens.float : ("s_expr", 1),
        Tokens.boolean : ("s_expr", 1),
        Tokens.integer : ("s_expr", 1),
        Tokens.operator : ("s_expr", 1),
        "\0" : ("s_expr", 1),
        "\"" : ("s_expr", 1),
        "'" : ("s_expr", 1),
        "(" : ("s_expr", 1),
        ")" : ("s_expr", 1)
    },
    goto_map = {}
)

parser.state_map[9] = Parser.State(
    lexer_state = lexer.state_map[17],
    shift_map = {},
    reduce_map = {
        Tokens.identifier : ("atom", 1),
        Tokens.float : ("atom", 1),
        Tokens.boolean : ("atom", 1),
        Tokens.integer : ("atom", 1),
        Tokens.operator : ("atom", 1),
        "\0" : ("atom", 1),
        "\"" : ("atom", 1),
        "'" : ("atom", 1),
        "(" : ("atom", 1),
        ")" : ("atom", 1)
    },
    goto_map = {}
)

parser.state_map[10] = Parser.State(
    lexer_state = lexer.state_map[4],
    shift_map = {
        Tokens.string : 11,
    },
    reduce_map = {},
    goto_map = {}
)

parser.state_map[11] = Parser.State(
    lexer_state = lexer.state_map[20],
    shift_map = {
        "\"" : 12
    },
    reduce_map = {},
    goto_map = {}
)

parser.state_map[12] = Parser.State(
    lexer_state = lexer.state_map[17],
    shift_map = {},
    reduce_map = {
        Tokens.identifier : ("atom", 3),
        Tokens.float : ("atom", 3),
        Tokens.boolean : ("atom", 3),
        Tokens.integer : ("atom", 3),
        Tokens.operator : ("atom", 3),
        "\0" : ("atom", 3),
        "\"" : ("atom", 3),
        "'" : ("atom", 3),
        "(" : ("atom", 3),
        ")" : ("atom", 3)
    },
    goto_map = {}
)

parser.state_map[13] = Parser.State(
    lexer_state = lexer.state_map[21],
    shift_map = {
        Tokens.boolean : 9,
        Tokens.float : 9,
        Tokens.identifier : 9,
        Tokens.integer : 9,
        Tokens.operator : 9,
        "\"" : 10,
        "(" : 15
    },
    reduce_map = {},
    goto_map = {
        "s_expr" : 14,
        "atom" : 8
    }
)

parser.state_map[14] = Parser.State(
    lexer_state = lexer.state_map[17],
    shift_map = {},
    reduce_map = {
        Tokens.identifier : ("qs_expr", 2),
        Tokens.float : ("qs_expr", 2),
        Tokens.boolean : ("qs_expr", 2),
        Tokens.integer : ("qs_expr", 2),
        Tokens.operator : ("qs_expr", 2),
        "\0" : ("qs_expr", 2),
        "\"" : ("qs_expr", 2),
        "'" : ("qs_expr", 2),
        "(" : ("qs_expr", 2),
        ")" : ("qs_expr", 2)
    },
    goto_map = {}
)

parser.state_map[15] = Parser.State(
    lexer_state = lexer.state_map[15],
    shift_map = {
        Tokens.boolean : 9,
        Tokens.float : 9,
        Tokens.identifier : 9,
        Tokens.integer : 9,
        Tokens.operator : 9,
        "\"" : 10,
        "'" : 13,
        "(" : 15
    },
    reduce_map = {},
    goto_map = {
        "list" : 16,
        "qs_expr" : 4,
        "s_expr" : 4,
        "atom" : 8
    }
)

parser.state_map[16] = Parser.State(
    lexer_state = lexer.state_map[19],
    shift_map = {
        ")" : 17
    },
    reduce_map = {},
    goto_map = {}
)

parser.state_map[17] = Parser.State(
    lexer_state = lexer.state_map[17],
    shift_map = {},
    reduce_map = {
        Tokens.identifier : ("s_expr", 3),
        Tokens.float : ("s_expr", 3),
        Tokens.boolean : ("s_expr", 3),
        Tokens.integer : ("s_expr", 3),
        Tokens.operator : ("s_expr", 3),
        "\0" : ("s_expr", 3),
        "\"" : ("s_expr", 3),
        "'" : ("s_expr", 3),
        "(" : ("s_expr", 3),
        ")" : ("s_expr", 3)
    },
    goto_map = {}
)

