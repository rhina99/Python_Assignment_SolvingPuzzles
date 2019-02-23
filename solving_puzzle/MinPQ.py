class MinPQ(list):
    '''A min-heap implementation of a priority queue.'''
    def insert(self, item):
        '''Add an item to the priority queue. The algorithm
        simply adds it to the end of the Python list, and then
        'raises' the value to restore the heap ordering property.'''
        self.append(item)
        self._raise(self, len(self) - 1)

    def delMin(self):
        '''Delete the minimum item from the priority queue. To
        restore the heap ordering property, the last element on
        the heap is swapped into the initial position, and then
        'lowers' itself to a legal position.'''
        r = self[0]             # get root (smallest element)
        t = self.pop()          # remove last element
        if self:                # if not empty.
            self[0] = t         # replace root
            self._lower(self, 0, len(self))
        return r

    def isEmpty(self):
        '''Returns True if queue is empty.'''
        return self == []

    @staticmethod
    def _parent(k):
        '''Returns the index of the parent of a node.'''
        return (k - 1) // 2

    @staticmethod
    def _lchild(k):
        '''Returns the index of the left child of a node.'''
        return (k * 2) + 1

    @staticmethod
    def _rchild(k):
        '''Returns the index of the right child of a node.'''
        return (k * 2) + 2

    @classmethod
    def _raise(cls, data, k):
        '''Raise an item from position 'k' until the heap
        ordering property is satisfied. Requires at most
        log2(k) iterations.'''
        j = cls._parent(k)
        while k > 0 and data[j] > data[k]:
            data[j], data[k] = data[k], data[j]
            k = j
            j = cls._parent(k)

    @classmethod
    def _lower(cls, data, k, n):
        '''Lower an item from position 'k' until the heap
        ordering property is satisfied. Requires at most
        log2(n) iterations.'''
        j = cls._lchild(k)
        while j < n:            # while left child in heap.
            # Use the lesser of the left and right children.
            if j < n - 1 and data[j] > data[j + 1]:
                j += 1
            if data[k] <= data[j]:
                break
            data[j], data[k] = data[k], data[j] # exchange.
            k = j
            j = cls._lchild(k)
