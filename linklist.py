class Empty(Exception):
    pass


class LinkedStack:
    class _Node:
        __slots__ = '_element', '_next'

        def __init__(self, element, next_node):
            self._element = element
            self._next = next_node
    
    def __init__(self):
        self._head = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0 

    def push(self, e):
        self._head = self._Node(e, self._head)
        self._size += 1

    def top(self):
        if self.is_empty():
            raise Empty('Stack is empty')

        return self._head._element

    def pop(self):
        if self.is_empty():
            raise Empty('Stack is empty')

        answer = self._head._element
        self._head = self._head._next
        self._size -= 1
        return answer


class LinkQueue:
    class _Node:
        __slots__ = '_element', '_next'

        def __init__(self, element, next_node):
            self._element = element
            self._next = next_node

    def __init__(self):
        self._head = None
        self._tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def first(self):
        if self.is_empty():
            raise Empty('Queue is empty')
        return self._head._element

    def enqueue(self, e):
        newest = self._Node(e, None)
        if self._head == None:
            self._head = newest
        else:
            self._tail._next = newest
        self._tail = newest
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise Empty('Queue is empty')

        answer = self._head._element
        self._head = self._head._next
        self._size -= 1
        if self.is_empty():
            self._tail = None
        return answer


class CircularQueue:

    class _Node:
        __slots__ = '_element', '_next'

        def __init__(self, element, next_node):
            self._element = element
            self._next = next_node

    def __init__(self):
        # self._head = None
        self._tail = None
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def first(self):
        if self.is_empty():
            raise Empty('Queue is empty')

        head = self._tail._next
        return head._element

    def enqueue(self, e):
        newest = self._Node(e, None)
        if self.is_empty():
            newest._next = newest
        else:
            newest._next = self._tail._next
            self._tail._next = newest
        self._tail = newest
        self._size += 1

    def dequeue(self):
        if self.is_empty():
            raise Empty('Queue is empty')

        oldhead = self._tail._next
        if self._size == 1:
            self._tail = None
        else:
            self._tail._next = oldhead._next
        self._size -= 1
        return oldhead._element

    def rotate(self):
        if self._size > 1:
            self._tail = self._tail._next
    

class _DoublyLinkedBase:
    class _Node:
        __slots__ = '_element', '_prev', '_next'

        def __init__(self, element, prev, next_node):
            self._element = element
            self._prev = prev
            self._next = next_node

    def __init__(self):
        self._header = self._Node(None, None, None)
        self._tailer = self._Node(None, None, None)
        self._header._next = self._tailer
        self._tailer._prev = self._header
        self._size = 0

    def __len__(self):
        return self._size

    def is_empty(self):
        return self._size == 0

    def _insert_between(self, e, predecessor, successor):
        newest = self._Node(e, predecessor, successor)
        predecessor._next = newest
        successor._prev = newest
        self._size += 1
        return newest

    def _delete_node(self, node):
        predecessor = node._prev
        successor = node._next
        predecessor._next = successor
        successor._prev = predecessor
        self._size -= 1
        element = node._element
        node._prev = node._next = node._element = None
        return element


class LinkedQueue(_DoublyLinkedBase):
    def first(self):
        if self.is_empty():
            raise Empty('Queue is empty')
        return self._header._next._element

    def last(self):
        if self.is_empty():
            raise Empty('Queue is empty')
        return self._tailer._prev._element

    def insert_first(self, e):
        self._insert_between(e, self._header, self._header._next)

    def insert_last(self, e):
        self._insert_between(e, self._tailer._prev, self._tailer)

    def delete_first(self):
        if self.is_empty():
            raise Empty('Queue is empty')
        return self._delete_node(self._header._next)

    def delete_last(self):
        if self.is_empty():
            raise Empty('Queue is empty')
        return self._delete_node(self._tailer._prev)



class PositionalList(_DoublyLinkedBase):

    class Position:
        def __init__(self, container, node):
            self._container = container
            self._node = node

        def element(self):
            return self._node._element

        def __eq__(self, other):
            return type(other) is type(self) and other._node is self._node
        
        def __ne__(elf, other):
            return not (self == other)


    # utility method

    def _validate(self, p):
        if not isinstance(p, self.Position):
            raise TypeError('p must be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._node._next is None:
            raise ValueError('p is no longer valid')
        return p._Node

    def _make_position(self, node):
        if node is self._header or node is self._tailer:
            return None
        else:
            return self.Position(self, node)

    # accessors
    
    def first(self):
        return self._make_position(self._header._next)

    def last(self):
        return self._make_position(self._tailer._prev)

    def before(self, p):
        """Return the position just before postion p (or None if p is first)"""
        node = self._validate(p)
        return self._make_position(node._prev)

    def after(self, p):
        node = self._validate(p)
        return self._make_position(node._next)

    def __iter__(self):
        curor = self.first()
        while curor is not None:
            yield curor.element()
            cursor = self.after(curor)

    # mutators

    def _insert_between(self, e, predecessor, successor):
        node = super()._insert_between(e, predecessor, successor)
        return self._make_position(node)

    def add_first(self, e):
        return self._insert_between(e, self._header, self._header._next)

    def add_last(self, e):
        return self._insert_between(e, self._tailer._prev, self._tailer)

    def add_before(self, p, e):
        """Insert element e into list before Posittion p and terturn new Position"""
        original = self._validate(p)
        return self._insert_between(e, original._prev, original)

    def add_after(self, p, e):
        original = self._validate(p)
        return self._insert_between(e, original, original._next)

    def delete(self, p):
        original = self._validate(p)
        return self._delete_node(original)

    def replace(self, p, e):
        original = self._validate(p)
        old_value = original._element
        original.element = e
        return old_value



class FavoriteList:

    class _Item:
        __slots__ = '_value', '_count'
        def __init__(self, e):
            self._value = e
            self._count = 0

    # nonpublic utilities

    def _find_position(self, e):
        walk = self._data.first()
        while walk is not None and walk.element()._value != e:
            walk = self._data.after(walk)
        return walk

    def _move_up(self, p):
        """Move item at Positon p earlier in the list baseed on access count"""
        if p != self._data.first():
            cnt = p.element()._count
            walk = self._data.before(p)
            if cnt > walk.element()._count:
                while (walk != self._data.first() and cnt > self._data.before(walk).element()._count):
                    walk = self._data.before(walk)
                self._data.add_before(walk, self._data.delete(p))

    # public methods

    def __init__(self):
        self._data = PositionalList()

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self._data) == 0

    def access(self, e):
        p = self._find_position(e)
        if p is None:
            p = self._data.add_last(self._Item(e))
        p.element()._count += 1
        self._move_up(p)

    def remove(self, e):
        p = self._find_position(e)
        if p is not None:
            self._data.delete(p)

    def top(self, k):
        if not 1 <= k <= len(self):
            raise ValueError('Illegal value for k')

        walk = self._data.first()
        for j in range(k):
            item = walk.element()
            yield item._value
            item = self._data.after(walk)


class FavoriteListMTF(FavoriteList):
    def _move_up(self, p):
        if p != self._data.first():
            self._data.add_first(self._data.delete(p))

    def top(self, k):
        if not 1 <= k <= len(self):
            raise ValueError('Illegal value for k')
        temp = PositionalList()
        for item in self._data:
            temp.add_last(item)
        
        # We repeatedly find, report, and remove element with largest count
        for j in range(k):
            # Find and report next highest from temp
            highPos = temp.first()
            walk = temp.after(highPos)
            while walk is not None:
                if walk.element()._count > highPos.element()._count:
                    highPos = walk
                walk = temp.after(walk)

            # We have found the element with highest count
            yield highPos.element()._value
            temp.delete(highPos)