
class Node:
    def __init__(this, val = None, car = None, cdr = None):
        this.val = val
        this.car = car
        this.cdr = cdr

def val(node):
    return None if node is None else node.val

def car(node):
    return None if node is None else node.car

def cdr(node):
    return None if node is None else node.cdr

def caar(node):
    return car(car(node))

def cadr(node):
    return cdr(car(node))

def cddr(node):
    return cdr(cdr(node))

def iter_cdr(node, exclude = None, reverse = False):
    if reverse == False:
        it_node = node
        while it_node:
            if exclude is None or exclude(it_node) == False:
                yield it_node
            it_node = cdr(it_node)
    else:
        node_arr = [node for node in iter_cdr(node)]
        while node_arr:
            yield node_arr.pop()

