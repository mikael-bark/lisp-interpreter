
from lisp_parser import parser
from helpers import iter_cdr, Node
from graph import Graph

class AbstractSyntaxTree(Graph):
    def __init__(self, root):
        super.__init__(root)

    class ProgramNode(Node):
        def __init__(self, parse_node):
            Node.__init__(self)

        def __str__(self):
            return "program"

    class ListNode(Node):
        def __init__(self, ast_node = None):
            Node.__init__(self)
            if ast_node:
                self.car = ast_node.car
                self.cdr = ast_node.cdr

        def __str__(self):
            return "list"

    class DefunNode(Node):
        def __init__(self, ast_node):
            Node.__init__(self)
            self.car = ast_node.car.cdr
            self.cdr = ast_node.cdr
            assert type(self.car) == AbstractSyntaxTree.IdentifierNode
            self.name = self.car.name
            self.lambda_expr =\
                AbstractSyntaxTree.LambdaNode(self.car.cdr)
            self.car.cdr = self.lambda_expr

        def __str__(self):
            return "defun"

    class OperatorNode(Node):
        def __init__(self, parse_node):
            Node.__init__(self)
            operator_node = parse_node.car
            self.name = parse_node.value
        node_is_operator =\
            lambda node:\
                True if node.name == "list" and\
                        car(node) != None and\
                        car(node).name == "identifier" and\
                        car(node).str in builtin_map\
                        else False

        def __str__(self):
            return "defun"

    class BuiltinNode(Node):
        def __init__(self, ast_node):
            Node.__init__(self)
            self.name = ast_node.car.name
            self.car = ast_node.car.cdr
            self.cdr = ast_node.cdr

        def __str__(self):
            return "builtin"

    class NullNode(Node):
        def __init__(self, parse_node):
            Node.__init__(self)
            self.cdr = parse_node.cdr

        def __str__(self):
            return "null"

    class ConditionalNode(Node):
        def __init__(self, ast_node):
            Node.__init__(self)
            self.car = ast_node.car.cdr
            self.predicate_expr = self.car
            self.left_expr = ast_node.car.cdr.cdr
            self.right_expr = ast_node.car.cdr.cdr.cdr
        node_is_conditional =\
            lambda node:\
                True if node.name == "list" and\
                        car(node) != None and\
                        car(node).name == "identifier" and\
                        car(node).str == "if"\
                        else False

        def __str__(self):
            return "if-conditional"

    class LambdaNode(Node):
        def __init__(self, ast_node):
            Node.__init__(self)
            self.car = ast_node
            self.param_list = ast_node
            assert type(self.param_list) == AbstractSyntaxTree.ListNode
            self.body_expr = ast_node.cdr
        node_is_lambda =\
            lambda node:\
                True if node.name == "list" and\
                        car(node) != None and\
                        car(node).name == "identifier" and\
                        car(node).str == "lambda"\
                        else False

        def __str__(self):
            return "lambda"

    class IdentifierNode(Node):
        def __init__(self, parse_node):
            Node.__init__(self)
            self.name = parse_node.value

        def __str__(self):
            return "identifier"

    class IntegerNode(Node):
        def __init__(self, parse_node):
            Node.__init__(self)
            self.value = int(parse_node.value)

        def __str__(self):
            return "integer"

    class BooleanNode(Node):
        def __init__(self, parse_node):
            Node.__init__(this)
            this.value = value

        def __str__(self):
            return "boolean"

    class StringNode(Node):
        def __init__(self, parse_node):
            Node.__init__(self)
            self.value = value

        def __str__(self):
            return "string"

is_identifier =\
    lambda ast_node:\
        True if type(ast_node) == AbstractSyntaxTree.IdentifierNode else False

is_operator =\
    lambda ast_node:\
        True if type(ast_node) == AbstractSyntaxTree.OperatorNode else False

builtin_name_set = set([
    "ash", "plus", "minus", "begin", "cons",
    "eqv?", "null?", "list", "print", "car",
    "cdr", "cadr", "cddr", "caddr", "cdddr"
])

def ast_atom_type(parse_node):
    atom_ast_type_map = {
        "boolean": AbstractSyntaxTree.BooleanNode,
        "identifier": AbstractSyntaxTree.IdentifierNode,
        "integer": AbstractSyntaxTree.IntegerNode,
        "operator": AbstractSyntaxTree.OperatorNode,
        "string": AbstractSyntaxTree.StringNode
    }
    assert parse_node.car
    if parse_node.car.name == "identifier" and parse_node.car.value == "NIL":
        return AbstractSyntaxTree.NullNode
    elif parse_node.car.name in atom_ast_type_map:
        return atom_ast_type_map[parse_node.car.name]
    else:
        assert False

def convert_list_ast(list_ast_node):
    assert list_ast_node.car
    if is_identifier(list_ast_node.car):
        list_type_map = {
            "if": AbstractSyntaxTree.ConditionalNode,
            "defun": AbstractSyntaxTree.DefunNode,
            "lambda": AbstractSyntaxTree.LambdaNode,
            "conditional": AbstractSyntaxTree.ConditionalNode
        }
        identifier_node = list_ast_node.car
        if identifier_node.name == "lambda":
            lambda_node = list_type_map[identifier_node.name](list_ast_node.car.cdr)
            lambda_node.cdr = list_ast_node.cdr
            return lambda_node
        elif identifier_node.name in list_type_map:
            return list_type_map[identifier_node.name](list_ast_node)
        elif identifier_node.name in builtin_name_set:
            return AbstractSyntaxTree.BuiltinNode(list_ast_node)
    elif is_operator(list_ast_node.car):
        operator_builtin_map = {
            "-": "minus",
            "+": "plus"
        }
        list_ast_node.car.name = operator_builtin_map[list_ast_node.car.name]
        return AbstractSyntaxTree.BuiltinNode(list_ast_node)
    return AbstractSyntaxTree.ListNode(list_ast_node)

def create_ast(parse_tree):
    ast_node_map = {}
    for parse_node in parse_tree.iter_postorder(unique_val = False):
        if parse_node.name == "atom":
            assert parse_node.car
            ast_node = ast_atom_type(parse_node)(parse_node.car)
            ast_node_map[parse_node] = ast_node
            if parse_node.cdr:
                assert parse_node.cdr in ast_node_map
                ast_node.cdr = ast_node_map[parse_node.cdr]
        elif parse_node.name == "list":
            assert parse_node.car
            ast_node = AbstractSyntaxTree.ListNode()
            ast_node_map[parse_node] = ast_node
            if parse_node.car:
                assert parse_node.car in ast_node_map
                ast_node.car = ast_node_map[parse_node.car]
            if parse_node.cdr:
                assert parse_node.cdr in ast_node_map
                ast_node.cdr = ast_node_map[parse_node.cdr]
    return Graph(ast_node_map[parse_tree.root.car])

def convert_lists(ast_tree):
    def convert(ast_node, parent, sibling):
        if type(ast_node) == AbstractSyntaxTree.ListNode:
            new_ast_node = convert_list_ast(ast_node)
            if sibling:
                sibling.cdr = new_ast_node
            elif parent:
                parent.car = new_ast_node
    ast_tree.visit_postorder(
        convert,
        child_first = True,
        unique_val = False)

def print_tree(tree):
    for node, depth in zip(tree.iter_preorder(unique_val = False), tree.iter_depth(unique_val = False)):
        print("    " * depth, node)
    print()

def program_callback(node):
    pass

def list_callback(node):
    if node.car.cdr:
        node.car.cdr = node.car.cdr.car
    assert node.car.name == "s_expr"
    for child in iter_cdr(node.car, reverse = True):
        if child.name == "s_expr":
            s_expr = child
            assert s_expr.name == "s_expr"
            if s_expr.cdr and s_expr.cdr.name == "s_expr":
                s_expr.cdr = s_expr.cdr.car
            s_expr.car.cdr = s_expr.cdr
    assert node.car.name == "s_expr"
    node.car = node.car.car

def s_expr_callback(node):
    pass

parser.callback_map["list"] = list_callback
parser.callback_map["s_expr"] = s_expr_callback
parser.callback_map["program"] = program_callback

parse_tree = Graph(parser.parse())
ast_tree = create_ast(parse_tree)
convert_lists(ast_tree)
print_tree(ast_tree)

