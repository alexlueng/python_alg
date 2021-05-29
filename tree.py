from typing import Type
from linklist import LinkedQueue

class Tree:
    """
        Abstract base class representing a tree structure
    """

    class Position:
        
        def element(self):
            raise NotImplementedError('must be implemented by subclass')

        def __eq__(self, other):
            raise NotImplementedError('must be implemented by subclass')

        def __ne__(self, other):
            return not(self==other)

    #----------- abstract methods that concrete subclass must support -----
    def root(self):
        raise NotImplementedError('must be implemented by subclass')
    def parent(self, p):
        raise NotImplementedError('must be implemented by subclass')
    def num_children(self, p):
        raise NotImplementedError('must be implemented by subclass')
    def children(self, p):
        raise NotImplementedError('must be implemented by subclass')
    def __len__(self):
        raise NotImplementedError('must be implemented by subclass')

    #---------- concrete methods impplemented in this class -------

    def is_root(self, p):
        return self.root == p
    def is_leaf(self, p):
        return self.num_children(p) == 0
    def is_empty(self):
        return len(self) == 0

    def __iter__(self):
        for p in self.Positions:
            yield p.element

    def preorder(self):
        if not self.is_empty():
            for p in self._subtree_preorder(self.root()):
                yield p
    
    def _subtree_preorder(self, p):
        yield p
        for c in self.children(p):
            for other in self._subtree_preorder(c):
                yield other

    def postorder(self, p):
        if not self.is_empty():
            for p in self._subtree_postorder(self.root()):
                yield p

    def _subtree_postorder(self, p):
        for c in self.children(p):
            for other in self._subtree_postorder(c):
                yield other
        yield p

    def Positions(self):
        return self.preorder() # default order way

    def breadthfirst(self):
        if not self.is_empty():
            fringe = LinkedQueue()
            fringe.enqueue(self.root())
            while not fringe.is_empty():
                p = fringe.dequeue()
                yield p
                for c in self.children(p):
                    fringe.enqueue(c)


class BinaryTree(Tree):
    
    #---------- Additional abstract methods----
    def left(self, p):
        raise NotImplementedError('must be implemented by subclass')

    def right(self, p):
        raise NotImplementedError('must be implemented by subclass')

    #---------- Concrete methods
    def sibling(self, p):
        """Return a Position representing p's sibling (or none if no sibling)"""
        parent = self.parent(p)
        if parent is None:
            return None
        else:
            if p == self.left(parent):
                return self.right(parent)
            else:
                return self.left(parent)

    def children(self, p):
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)

    def inorder(self):
        if not self.is_empty():
            for p in self._subtree_inorder(self.root()):
                yield p

    def _subtree_inorder(self, p):

        if self.left(p) is not None:
            for other in self._subtree_inorder(self.left(p)):
                yield other

        yield p

        if self.right(p) is not None:
            for other in self._subtree_inorder(self.right(p)):
                yield other
    

class LinkedBinaryTree(BinaryTree):

    class _Node:
        __slots__ = '_element', '_parent', '_left', '_right'
        def __init__(self, element, parent=None, left=None, right=None) -> None:
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    class Position(BinaryTree.Position):
        """An abstraction representing the location of a a single element"""
        def __init__(self, container, node):
            self._container = container
            self._node = node

        def element(self):
            return self._node._element

        def __eq__(self, other):
            return type(other) is type(self) and other._node is self._node
    
    def _validate(self, p):
        """Return associated node, if position is valid"""
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._node._parent is p._node:
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self, node):
        return self.Position(self, node) if node is not None else None

    #---------- binary tree constructor --------------
    def __init__(self):
        self._root = None
        self._size = 0

    #---------- public accessors ---------------------
    def __len__(self):
        return self._size
    
    def root(self):
        return self._make_position(self._root)

    def parent(self, p):
        node = self._validate(p)
        return self._make_position(node._parent)

    def left(self, p):
        node = self._validate(p)
        return self._make_position(node._left)
    
    def right(self, p):
        node = self._validate(p)
        return self._make_position(node._right)

    def num_children(self, p):
        node = self._validate(p)
        count = 0
        if node._left is not None:
            count += 1
        if node._right is not None:
            count += 1
        return count

    #------------maniplate the thee
    def _add_root(self, e):
        if self._root is not None:
            raise ValueError('Root exist')
        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)

    def _add_left(self, p, e):
        node = self._validate(p)
        if node._left is not None:
            raise ValueError('Left child exists')
        self._size += 1
        node._left = self._Node(e)
        return self._make_position(node._left)

    def _add_right(self, p, e):
        node = self._validate(p)
        if node._right is not None:
            raise ValueError('Right child exists')
        self._size += 1
        node._left = self._Node(e)
        return self._make_position(node._right)

    def _replace(self, p, e):
        node = self._validate(p)
        old = node._element
        node._element = e
        return old 

    def _delete(self, p):
        node = self._validate(p)
        if self.num_children(p) == 2:
            raise ValueError('p has two children')

        child = node.left if node._left else node._right
        if child is not None:
            child._parent = node._parent
        if node is self._root:
            self._root = child
        else:
            parent = node._parent
            if node is parent._left:
                parent._left = node
            else:
                parent._right = node
        self._size -= 1
        node._parent = node
        return node._element

    def _attach(self, p, t1, t2):
        node = self._validate(p)
        if not self._is_leaf(p):
            raise ValueError('position must be leaf')
        if not type(self) is type(t1) is type(t2):
            raise TypeError('Tree types must match')
        self._size += len(t1) + len(t2)
        if not t1.is_empty():
            t1._root._parent = node
            t1._root = None
            t1._size = 0
        if not t2.is_empty():
            t2._root._parent = node
            t2._root = None
            t2._size = 0


    # 树的深度和高度
    def depth(self):
        ...
    def height(self):
        ...