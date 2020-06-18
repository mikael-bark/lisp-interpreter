
import itertools
import sys
from lisp_ast import ast_tree, AbstractSyntaxTree
from helpers import iter_cdr, Node
from graph import Graph

class Env:
    def __init__(self):
        self.env_stack = []
        self.env_stack.append({})

    def new_scope(self):
        self.env_stack.append({})

    def pop_scope(self):
        assert self.env_stack
        self.env_stack.pop()

    def bind(self, params, args):
        for param_name, arg_node in zip(params, args):
            assert type(param_name) == str
            self.env_stack[-1][param_name] = arg_node

    def lookup(self, symbol_name):
        for env in reversed(self.env_stack):
            if symbol_name in env:
                return env[symbol_name]
        print("Error: Lookup of ", symbol_name, " failed", sep = '')
        assert False

builtin_map = {
    'ash'   : lambda args: args[0] << args[1],
    'begin' : lambda args: args[-1],
    'car'   : lambda args: args[0][:1],
    'cdr'   : lambda args: args[0][1:],
    'cadr'  : lambda args: args[0][1:][0] if args[0][1:] else [],
    'cddr'  : lambda args: args[0][2:],
    'caddr' : lambda args: args[0][2:][0] if args[0][2:] else [],
    'cons'  : lambda args: args[0] + args[1],
    'eqv?'  : lambda args: args[0] == args[1],
    'list'  : lambda args: args,
    'minus' : lambda args: args[0] - args[1],
    'null?' : lambda args: args[0] == [],
    'plus'  : lambda args: args[0] + args[1],
    'print' : lambda args: print(*args)
}

environ = Env()

def eval_defun(defun_node):
    #print("Eval Defun")
    environ.bind(
        [defun_node.name],
        [defun_node.lambda_expr])

def eval_identifier(identifier_node):
    #print("Eval Identifier")
    #print("    ", identifier_node.name)
    result = environ.lookup(identifier_node.name)
    #print("    identifier", identifier_node.name, "is", result)
    return result

def eval_integer(integer_node):
    #print("Eval Integer", integer_node.value)
    return integer_node.value

def eval_null(null_node):
    #print("Eval NULL")
    return []

def eval_builtin(builtin_node):
    #print("Eval builtin", builtin_node.name)
    eval_arr = []
    for expr in iter_cdr(builtin_node.car):
        eval_arr.append(eval_expr(expr))
    builtin_lambda = builtin_map[builtin_node.name]
    result = builtin_lambda(eval_arr)
    return result

def eval_conditional(conditional_node):
    #print("Eval Conditional")
    predicate =\
        eval_expr(conditional_node.predicate_expr)
    #print("    predicate is", predicate)
    if predicate == True:
        return eval_expr(conditional_node.left_expr)
    elif predicate == False:
        return eval_expr(conditional_node.right_expr)

def eval_lambda(lambda_node, arg_arr):
    #print("Eval Lambda")
    environ.new_scope()
    param_arr = [param.name for param in iter_cdr(lambda_node.param_list.car)]
    #print("    bind:", param_arr, arg_arr)
    environ.bind(param_arr, arg_arr)
    for body_expr in iter_cdr(lambda_node.body_expr):
        result = eval_expr(body_expr)
    environ.pop_scope()
    #print("lambda returning:", result)
    return result

def eval_list(list_node):
    #print("Eval List")
    eval_arr = []
    for expr in iter_cdr(list_node.car):
        #print("eval", expr)
        if type(expr) != AbstractSyntaxTree.LambdaNode:
            eval_arr.append(eval_expr(expr))
        else:
            eval_arr.append(expr)
    #print("first eval:", type(eval_arr[0]))
    if type(eval_arr[0]) == AbstractSyntaxTree.LambdaNode:
        #print("eval lambda", eval_arr)
        return eval_lambda(eval_arr[0], eval_arr[1:])

def eval_expr(expr_node):
    eval_map = {
        AbstractSyntaxTree.DefunNode: eval_defun,
        AbstractSyntaxTree.IdentifierNode: eval_identifier,
        AbstractSyntaxTree.IntegerNode: eval_integer,
        AbstractSyntaxTree.NullNode: eval_null,
        AbstractSyntaxTree.BuiltinNode: eval_builtin,
        AbstractSyntaxTree.ConditionalNode: eval_conditional,
        AbstractSyntaxTree.ListNode: eval_list
    }
    assert type(expr_node) in eval_map
    return eval_map[type(expr_node)](expr_node)


eval_expr(ast_tree.root)
print("OK!")

