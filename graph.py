
from helpers import *

class Graph:
    def __init__(this):
        this.root = None
        this.print_node = None

    def __init__(this, root):
        this.root = root
        this.nodes = []
        this.node_count = 0
        this.print_node = None

    def append_node(this, node):
        this.nodes += [node]
        this.node_count += 1

    #def traverse_preorder(this, left_first = True, start_node = None, exclude = None):
    #    #print("traverse preorder")
    #    stack = []
    #    if start_node:
    #        stack.append(start_node)
    #    else:
    #        stack.append(this.root)
    #    visited = set()
    #    while stack:
    #        node = stack.pop()
    #        if exclude and exclude(node) == True:
    #            continue
    #        if node not in visited:
    #            visited.add(node)
    #            #print("  yield preorder", node.order)
    #            yield node
    #        else:
    #            continue
    #        first = node.cdr if left_first else node.car
    #        second = node.car if left_first else node.cdr
    #        if first is not None:
    #            stack.append(first)
    #        if second is not None:
    #            stack.append(second)

    #def traverse_preorder2(this, left_first = True, start_node = None, exclude = None):
    #    stack = []
    #    if start_node:
    #        stack.append(start_node)
    #    else:
    #        stack.append(this.root)
    #    visited = set()
    #    while stack:
    #        #print("stack: ", end = '')
    #        #for node in stack:
    #        #    print(node.ind, " ", end = '')
    #        #print()
    #        node = stack.pop()
    #        if exclude:
    #            if exclude(node) == True:
    #                continue
    #        if node not in visited:
    #            visited.add(node)
    #            #print(node.ind, " ", end = '')
    #            #if node.car:
    #            #    print("car ", node.car.ind, " ", end = '')
    #            #if node.cdr:
    #            #    print("cdr ", node.cdr.ind, " ", end = '')
    #            yield node
    #        else:
    #            continue
    #        first = node.cdr if left_first else node.car
    #        second = node.car if left_first else node.cdr
    #        if first is not None:
    #            stack.append(first)
    #        if second is not None:
    #            stack.append(second)

    def iter_preorder(this,
        left_first = True,
        start_node = None,
        prune_filter = None,
        unique_val = True):
        stack = []
        if start_node:
            stack.append(start_node)
        else:
            stack.append(this.root)
        visited = set()
        while stack:
            node = stack.pop()
            if prune_filter and prune_filter(node) == True:
                continue
            if unique_val == True:
                if val(node) in visited:
                    continue
                visited.add(val(node))
            else:
                if node in visited:
                    continue
                visited.add(node)
            yield node
            first = node.cdr if left_first else node.car
            second = node.car if left_first else node.cdr
            if first is not None:
                stack.append(first)
            if second is not None:
                stack.append(second)

    #def traverse_inorder(this, left_first = True, start_node = None, exclude = None):
    #    stack = [] 
    #    node = this.root 

    #    while node is not None:
    #        stack.append(node)
    #        node = node.car
    #        while stack and node is None:
    #            node = stack.pop()
    #            yield node
    #            node = node.cdr

#    def traverse_inorder(this, left_first = True, start_node = None, exclude = None):
#        if start_node == None:
#            start_node = this.root
#        #print("traverse inorder")
#
#        node_iter =\
#            this.traverse_preorder(
#                left_first, start_node, exclude)
#        stack = [next(node_iter)]
#        visited = set()
#        #print()
#        for node in node_iter:
#            #print("node", node.ind)
#            # XXX change this to while stack[-1].cdr != node
#            while stack and\
#                stack[-1].car != node and\
#                stack[-1].cdr != node:
#                    yield stack.pop()
#            first = lambda node: cdr(node) if left_first else car(node)
#            if stack and first(stack[-1]) == node:
#                #print("  yield inorder node", stack[-1].order)
#                yield stack.pop()
#            stack.append(node)
#        while stack:
#            #print("  yield inorder node", stack[-1].order)
#            yield stack.pop()

    def iter_inorder(this,
        left_first = True,
        start_node = None,
        exclude = None,
        unique_val = True):
        if start_node == None:
            start_node = this.root
        #print("traverse inorder")

        node_iter =\
            this.iter_preorder(
                left_first, start_node, exclude, unique_val)
        stack = [next(node_iter)]
        visited = set()
        #print()
        for node in node_iter:
            #print("preorder node", node.val)
            # XXX change this to while stack[-1].cdr != node
            while stack and\
                stack[-1].car != node and\
                stack[-1].cdr != node:
                    #print("  yield inorder node", stack[-1].val)
                    yield stack.pop()
            first = lambda node: cdr(node) if left_first else car(node)
            if stack and first(stack[-1]) == node:
                #print("  yield inorder node", stack[-1].val)
                yield stack.pop()
            stack.append(node)
        while stack:
            #print("  yield inorder node", stack[-1].order)
            yield stack.pop()

    def iter_postorder(this,
      left_first = True,
      start_node = None,
      exclude = None,
      unique_val = True):
        stack = []
        visited = set()
        iter_preorder =\
            this.iter_preorder(left_first, start_node, exclude, unique_val)
        for node in iter_preorder:
            while stack and \
                stack[-1].car != node and \
                stack[-1].cdr != node:
                    yield stack.pop()
            stack.append(node)
        while stack:
            yield stack.pop()

    def iter_postorder2(this,
      left_first = True,
      start_node = None,
      exclude = None,
      unique_val = True):
        stack = []
        visited = set()
        iter_preorder =\
            this.iter_preorder(left_first, start_node, exclude, unique_val)
        for node in iter_preorder:
            print("preorder", node.uid)
            while stack and \
                stack[-1].car != node and \
                stack[-1].cdr != node:
                    yield stack.pop()
            stack.append(node)
        while stack:
            yield stack.pop()

    def iter_path(this, left_first = True, start_node = None, exclude = None):
        stack = []
        if start_node:
            stack.append(start_node)
        else:
            stack.append(this.root)
        path = []
        visited = set()
        while stack:
            node = stack.pop()
            if node not in path:
                first = node.cdr if left_first else node.car
                second = node.car if left_first else node.cdr
                if first is not None and (node, first) not in visited:
                    visited.add((node, first))
                    stack.append(first)
                if second is not None and (node, second) not in visited:
                    visited.add((node, second))
                    stack.append(second)
            while path and \
                path[-1].car != node and \
                path[-1].cdr != node:
                    path.pop()
            path.append(node)
            yield path

    # Yields list of nodes that
    def iter_parent(this, left_first = True, start_node = None, unique_val = True):
        #print("iter preorder parent: left_first", left_first)
        parent = None
        if start_node == None:
            start_node = this.root
        iter_preorder =\
            this.iter_preorder(
                left_first,
                unique_val = unique_val)
        if left_first == True:
            iter_inorder =\
                this.iter_inorder(
                    left_first,
                    unique_val = unique_val)
            yield None
            inorder_node = next(iter_inorder)
            stack = [ next(iter_preorder) ]
            for preorder_node in iter_preorder:
                while stack and stack[-1] == inorder_node:
                    inorder_node = next(iter_inorder)
                    stack.pop()
                #print("  preorder node", preorder_node.order, "inorder node", inorder_node.order)
                if stack:
                    #print("yield node", preorder_node.order, "parent", stack[-1].order)
                    yield stack[-1]
                else:
                    #print("yield node", preorder_node.order, "parent None")
                    yield None
                stack.append(preorder_node)
        elif left_first == False:
            iter_postorder =\
                this.iter_postorder(
                    left_first = False,
                    unique_val = unique_val)
            postorder_node = next(iter_postorder)
            stack = [ next(iter_preorder) ]
            parent = None
            yield parent
            for preorder_node in iter_preorder:
                #print("  preorder node", preorder_node.order, "postorder node", postorder_node.order)
                if stack and stack[-1].car == preorder_node:
                    parent = stack[-1]
                #print("  yield preoder parent", parent.order)
                yield parent
                stack.append(preorder_node)
                while stack and stack[-1] == postorder_node:
                    #print("    popping", stack[-1].order, "postorder node", postorder_node.order)
                    postorder_node = next(iter_postorder)
                    stack.pop()

    #    inorder_node = next(iter_inorder)
    #    preorder_node = next(iter_preorder)

    #    path = [start_node]
    #    print("(", node.order, inorder_node.order, ")")
    #    yield None

    #    for node in iter_preorder:
    #        print("(", node.order, inorder_node.order, ")")
    #        if path:
    #            yield path[-1]
    #        else:
    #            yield None
    #        path.append(node)

    #        while path and path[-1] == inorder_node:
    #            node = path.pop()
    #            inorder_node = next(iter_inorder)

    def iter_parent_inorder(this, child_first = True, start_node = None, unique_val = True):
        if start_node is None:
            start_node = this.root
        iter_preorder =\
            zip(this.iter_preorder(
                    left_first = child_first,
                    start_node = start_node,
                    unique_val = unique_val),
                this.iter_parent(
                    left_first = child_first,
                    start_node = start_node,
                    unique_val = unique_val))
        iter_inorder =\
            this.iter_inorder(
                left_first = child_first,
                start_node = start_node,
                unique_val = unique_val)
        node_stack = []
        parent_stack = []
        inorder_node = next(iter_inorder)
        for preorder_node, parent in iter_preorder:
            node_stack.append(preorder_node)
            parent_stack.append(parent)
            while node_stack and node_stack[-1] == inorder_node:
                #print("  iter_parent_inorder pop", node_stack[-1].order, "inorder_node", inorder_node.order)
                node_stack.pop()
                yield parent_stack.pop()
                inorder_node = next(iter_inorder)
#        for inorder_node in iter_inorder:
#            print("ITER_PARENT_INORDER: inorder_node", inorder_node.order)
#            for preorder_node, parent in iter_preorder:
#                #if parent:
#                    #print("received preorder_node", preorder_node.order, "parent", parent.order, "inorder node", inorder_node.order)
#                node_stack.append(preorder_node)
#                parent_stack.append(parent)
#                if node_stack and node_stack[-1] == inorder_node:
#                    break
#            while node_stack and node_stack[-1] == inorder_node:
#                print("  iter_parent_inorder pop", node_stack[-1].order, "inorder_node", inorder_node.order)
#                node_stack.pop()
#                #if parent_stack[-1]:
#                    #print("  iter_parent_inorder yield parent", parent_stack[-1].order)
#                yield parent_stack.pop()
#                inorder_node = next(iter_inorder)

    def iter_parent_postorder(this, child_first = True, start_node = None, unique_val = True):
        if start_node is None:
            start_node = this.root
        iter_preorder =\
            zip(this.iter_preorder(
                    left_first = child_first,
                    start_node = start_node,
                    unique_val = unique_val),
                this.iter_parent(
                    left_first = child_first,
                    start_node = start_node,
                    unique_val = unique_val))
        iter_postorder =\
            this.iter_postorder(
                left_first = child_first,
                start_node = start_node,
                unique_val = unique_val)
        node_stack = []
        parent_stack = []
        postorder_node = next(iter_postorder)
        for preorder_node, parent in iter_preorder:
            node_stack.append(preorder_node)
            parent_stack.append(parent)
            while node_stack and node_stack[-1] == postorder_node:
                node_stack.pop()
                yield parent_stack.pop()
                postorder_node = next(iter_postorder)

    def visit_inorder(this, visit_func, child_first = True, start_node = None):
        if start_node is None:
            start_node = this.root
        iter_inorder =\
            this.iter_inorder(
                left_first = child_first,
                start_node = start_node)
        nps_it =\
            zip(this.iter_inorder(
                    left_first = child_first,
                    start_node = start_node),
                this.iter_parent_inorder(
                    child_first = child_first,
                    start_node = start_node),
                this.iter_sibling_inorder(
                    child_first = child_first,
                    start_node = start_node))
        for node, parent, sibling in nps_it:
            if parent:
                parent_str = parent.order
            else:
                parent_str = "None"
            if sibling:
                sibling_str = sibling.order
            else:
                sibling_str = "None"
            #print("  callback", node.order, "parent", parent_str, "sibling", sibling_str)
            visit_func(node, parent, sibling)

    def get_postorder_arr(this,
        child_first = True,
        start_node = None,
        unique_val = True):
        node_arr = []
        node_iter = this.iter_postorder(
            left_first = child_first,
            start_node = start_node,
            unique_val = unique_val)
        for node in node_iter:
            node_arr.append(node)
        parent_arr = []
        parent_iter = this.iter_parent_postorder(
            child_first = child_first,
            start_node = start_node,
            unique_val = unique_val)
        for parent in parent_iter:
            parent_arr.append(parent)
        assert len(node_arr) == len(parent_arr)
        return node_arr, parent_arr

    def visit_postorder(this, visit_func,
        child_first = True,
        start_node = None,
        unique_val = True):
        if start_node is None:
            start_node = this.root

        node_arr = []
        node_iter = this.iter_postorder(
            left_first = child_first,
            start_node = start_node,
            unique_val = unique_val)
        for node in node_iter:
            node_arr.append(node)
        #parent_arr = []
        #parent_iter = this.iter_parent_postorder(
        #    child_first = child_first,
        #    start_node = start_node,
        #    unique_val = unique_val)
        #for parent in parent_iter:
        #    parent_arr.append(parent)
        #sibling_arr = []
        #sibling_iter = this.iter_sibling_postorder(
        #    child_first = child_first,
        #    start_node = start_node,
        #    unique_val = unique_val)
        #for sibling in sibling_iter:
        #    sibling_arr.append(sibling)
        #print("length of node arr:", len(node_arr), "length of parent arr:", len(parent_arr), "length of sibling arr:", len(sibling_arr))
        #assert len(node_arr) == len(parent_arr)

        nps_it =\
            zip(this.iter_postorder(
                    left_first = child_first,
                    start_node = start_node,
                    unique_val = unique_val),
                this.iter_parent_postorder(
                    child_first = child_first,
                    start_node = start_node,
                    unique_val = unique_val),
                this.iter_sibling_postorder(
                    child_first = child_first,
                    start_node = start_node,
                    unique_val = unique_val))
        for node, parent, sibling in nps_it:
            #print("call visit")
            visit_func(node, parent, sibling)

#    def iter_parent2(this):
#        iter_preorder = this.traverse_preorder(left_first = True)
#        iter_inorder = this.traverse_inorder()
#        inorder_node = next(iter_inorder)
#
#        node = next(iter_preorder)
#        path = [node]
#        yield None
#
#        print()
#        for node in iter_preorder:
#            print("node: ", node.ind, "inorder_node: ", inorder_node.ind)
#            print("path: ", end = '')
#            for bla in path:
#                print(bla.ind, " ", end = '')
#            print()
#            if path:
#                print("yield ", path[-1].ind)
#                yield path[-1]
#            else:
#                yield None
#            path.append(node)
#
#            while path and path[-1] == inorder_node:
#                node = path.pop()
#                inorder_node = next(iter_inorder)

    def iter_sibling(this, left_first = True, unique_val = False):
        iter_preorder =\
            this.iter_preorder(
                left_first = left_first,
                unique_val = unique_val)
        if left_first == True:
            iter_inorder =\
                this.iter_inorder(unique_val = unique_val)
            inorder_node = next(iter_inorder)
            node = next(iter_preorder)
            path = [node]
            yield None
            popped_node = None
            for node in iter_preorder:
                if popped_node and popped_node.cdr == node:
                    yield popped_node
                else:
                    yield None
                path.append(node)
                while path and path[-1] == inorder_node:
                    popped_node = path.pop()
                    inorder_node = next(iter_inorder)
        elif left_first == False:
            sibling = None
            for node in iter_preorder:
                if sibling and sibling.cdr == node:
                    yield sibling
                else:
                    yield None
                sibling = node

    def iter_sibling_inorder(this, child_first = True, start_node = None):
        if start_node is None:
            start_node = this.root
        iter_np =\
            zip(this.iter_inorder(
                    left_first = child_first,
                    start_node = start_node),
                this.iter_parent_inorder(
                    child_first = child_first,
                    start_node = start_node))
        for node, parent in iter_np:
            #if parent != None:
            #    print("parent", parent.name, parent.order)
            if parent == None or parent.car == node:
                yield None
            else:
                for sibling in iter_cdr(parent.car):
                    #print("    finding sibling", sibling.name)
                    if sibling.cdr == node:
                        yield sibling
                        break

    def iter_sibling_postorder(this, child_first = True, start_node = None, unique_val = True):
        if start_node is None:
            start_node = this.root
        iter_np =\
            zip(this.iter_postorder(
                    left_first = child_first,
                    start_node = start_node,
                    unique_val = unique_val),
                this.iter_parent_postorder(
                    child_first = child_first,
                    start_node = start_node,
                    unique_val = unique_val))
        for node, parent in iter_np:
            #print("postorder sibling")
            if parent == None:
                #print("  No parent")
                sibling = None
                for sibit in iter_cdr(start_node):
                    if sibit.cdr == node:
                        sibling = sibit
                if sibling:
                    #print("  yield sibling")
                    yield sibling
                else:
                    #print("  yield sibling")
                    yield None
            elif parent.car == node:
                #print("  yield sibling")
                yield None
            else:
                assert parent.car
                #print("  must have a sibling...", parent.car)
                for sibling in iter_cdr(parent.car):
                    #print("    looking for sibling...")
                    if sibling.cdr == node:
                        #print("  yield sibling")
                        yield sibling
                        break

    def iter_depth(this, start_node = None, unique_val = True):
        iter_preorder =\
            this.iter_preorder(
                left_first = True,
                start_node = start_node,
                unique_val = unique_val)
        iter_parent =\
            this.iter_parent(
                unique_val = unique_val)
        depth_map = {}
        for node, parent in zip(iter_preorder, iter_parent):
            if parent:
                depth = depth_map[parent] + 1
            else:
                depth = 0

            depth_map[node] = depth
            yield depth

    def iter_index(this):
        iter_preorder = this.iter_preorder(left_first = True)
        iter_sibling = this.iter_sibling()

        index_map = {}

        for node, sibling in zip(iter_preorder, iter_sibling):
            if sibling:
                index = index_map[sibling] + 1
            else:
                index = 0
                
            index_map[node] = index
            yield index

    def iter_childCount(this, traversal_order):
        for node in traversal_order:
            child = node.car
            count = 0
            while child:
                count += 1
                child = child.cdr
            yield count

    # Find strongly connected components within a graph component.
    #
    # edges:
    #     Must be the edges of the component to be used as input.
    #     I.e. all nodes connected by these edges must be reachable from the start
    #     node.
    def find_scc(self, start_node = None, node_condition = None):
        if start_node == None:
            start_node = self.root
        if start_node == None:
            return [], {}
        #def print_pair_node3(node):
        #    print("(", val(node)[0].ind, " ", val(node)[1].ind, ")", end = '')
        rank = 1
        rank_map = {}
        lowlink_map = {}
        preo_visited = set()
        is_preo_visited =\
            lambda node:\
                True if val(node) in preo_visited else False
        iter_preo = self.iter_preorder(prune_filter = is_preo_visited)
        stack = []
        node_stack = []
        onstack = set()
        ino_visited = set()
        is_ino_visited =\
            lambda node:\
                True if val(node) in ino_visited else False
        iter_ino = self.iter_inorder(exclude = is_ino_visited)
        ino_node = None
        component_map = {}
        root_arr = []
        for preo_node in iter_preo:
            preo_visited.add(val(preo_node))
            #print("preorder node", preo_node.val.uid)
            if node_condition and node_condition(preo_node) == False:
                #print("  skip node")
                continue
            rank_map[val(preo_node)] = rank
            lowlink_map[val(preo_node)] = rank
            rank += 1
            stack.append(preo_node)
            node_stack.append(preo_node)
            onstack.add(val(preo_node))
            if ino_node is None:
                ino_node = next(iter_ino)
                ino_visited.add(val(ino_node))
            #print("inorder node", ino_node.val.uid)
            #print(" top of stack", stack[-1].val.uid, "ino node", ino_node.val.uid)
            while stack and stack[-1] == ino_node:
                head = stack.pop()
                if stack:
                    ino_node = next(iter_ino)
                    ino_visited.add(val(ino_node))
                else:
                    ino_node = None
                #if ino_node:
                #    print("  pop head", head.val.uid, "ino node", ino_node.val.uid)
                #else:
                #    print("  pop head", head.val.uid, "ino node None")
                for child in iter_cdr(head.car):
                    #print("  child", child.val.uid)
                    if val(child) not in onstack:
                        continue
                    head_lowlink = lowlink_map[val(head)]
                    child_lowlink = lowlink_map[val(child)]
                    lowlink_map[val(head)] = min(head_lowlink, child_lowlink)
                head_lowlink = lowlink_map[val(head)]
                head_rank = rank_map[val(head)]
                #print("  lowlink:", head_lowlink)
                #print("  rank:", head_rank)
                if head_rank == head_lowlink:
                    component = []
                    while node_stack and node_stack[-1] != head:
                        scc_node = node_stack[-1]
                        #print("popping node off stack", scc_node.val)
                        scc_lowlink = lowlink_map[val(scc_node)]
                        onstack.remove(val(scc_node))
                        component.append(scc_node)
                        component_map[val(scc_node)] = component
                        node_stack.pop()
                    scc_root = node_stack.pop()
                    onstack.remove(val(scc_root))
                    self_linking =\
                        (scc_root.car == scc_root) or\
                        (scc_root.cdr == scc_root)
                    if component or self_linking:
                        root_arr.append(head)
                        component.append(scc_root)
                        component_map[val(scc_root)] = component
        return root_arr, component_map

#    # Find strongly connected components within a graph component.
#    #
#    # edges:
#    #     Must be the edges of the component to be used as input.
#    #     I.e. all nodes connected by these edges must be reachable from the start
#    #     node.
#    def find_scc(self, start_node, edge_condition = None):
#        rank = 1
#        rank_map = {}
#        lowlink_map = {}
#        iter_preorder =\
#            self.traverse_preorder(
#                start_node = start_node)
#        visited = set()
#        for node in iter_preorder:
#            if payload(node) in visited:
#                continue
#            visited.add(payload(node))
#            rank_map[payload(node)] = rank
#            lowlink_map[payload(node)] = rank
#            rank += 1
#            print("set rank:", payload(node), rank_map[payload(node)])
#        root_arr = []
#        popped = set()
#        component = []
#        component_map = {}
#        iter_inorder =\
#            self.traverse_inorder(
#                start_node = start_node,
#                left_first = True)
#        for head in iter_inorder:
#            for tail in iter_cdr(head.car):
#                exclude_edge =\
#                    edge_condition and edge_condition(head, tail) == False
#                if exclude_edge == True:
#                    print("  exclude edge (", head.uid, tail.uid, ")")
#                if payload(tail) in popped or exclude_edge == True:
#                    continue
#                head_lowlink = lowlink_map[payload(head)]
#                tail_lowlink = lowlink_map[payload(tail)]
#                lowlink_map[payload(head)] = min(head_lowlink, tail_lowlink)
#            head_lowlink = lowlink_map[payload(head)]
#            head_rank = rank_map[payload(head)]
#            print("look at head:", payload(head), "lowlink:", head_lowlink, "rank:", head_rank)
#            component.append(head)
#            component_map[head] = component
#            if head_rank == head_lowlink:
#                print("same rank and lowlink len of scc", len(component))
#                if len(component) == 1 and head.car != head and head.cdr != head:
#                    component_map[head] = None
#                else:
#                    print("FOUND ROOT", payload(head))
#                    root_arr.append(head)
#                popped.add(payload(head))
#                component = []
#        return root_arr, component_map

    def print(this, callback):
        it = enumerate(
            zip(this.iter_preorder(unique_val = False),
            this.iter_depth(unique_val = False)))
        for ind, (node, depth) in it:
            callback(ind, node, depth)

    def print_2(this, callback):
        it = enumerate(
            zip(this.iter_preorder(unique_val = False),
            this.iter_depth(unique_val = False)))
        for ind, (node, depth) in it:
            callback(ind, node, depth)

    def visit(this, callback, args = None, unique_val = False):
        iter_nodes = zip(
            this.iter_preorder(unique_val = unique_val),
            this.iter_parent(unique_val = unique_val),
            this.iter_sibling(unique_val = unique_val))
            
        for node, parent, sibling in iter_nodes:
            if args:
                callback(node, parent, sibling, args)
            else:
                callback(node, parent, sibling)

