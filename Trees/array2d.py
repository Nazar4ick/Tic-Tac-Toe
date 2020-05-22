import ctypes


class Array:
    """
    Class for representing arrays
    """
    def __init__(self, size):
        """
        Initializes a new array
        :param size: int
        """
        assert size > 0
        self._size = size
        arr = ctypes.py_object * size
        self._elements = arr()
        self.clear(None)

    def __len__(self):
        return self._size

    def __getitem__(self, index):
        assert 0 <= index < len(self)
        return self._elements[index]

    def __setitem__(self, index, value):
        assert 0 <= index < len(self)
        self._elements[index] = value

    def clear(self, value):
        """
        Clears all items of the array to the given value
        :param value:
        :return: None
        """
        for i in range(len(self)):
            self._elements[i] = value

    def __iter__(self):
        return _ArrayIterator(self._elements)


class _ArrayIterator:
    """
    Class for representing array iterators
    """
    def __init__(self, the_array):
        """
        Initializes a new array iterator
        :param the_array:
        """
        self.arr_ref = the_array
        self.cur_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.cur_index < len(self.arr_ref):
            item = self.arr_ref[self.cur_index]
            self.cur_index += 1
            return item
        else:
            raise StopIteration


class Array2D:
    """
    Class for representing 2D arrays
    """
    def __init__(self, num_rows, num_cols):
        """
        Initalizes a new array
        :param num_rows: int
        :param num_cols: int
        """
        self.rows = Array(num_rows)
        for i in range(num_rows):
            self.rows[i] = Array(num_cols)

    def num_rows(self):
        """
        returns the number of rows in the array
        :return: int
        """
        return len(self.rows)

    def num_cols(self):
        """
        returns the number of columns in the array
        :return: int
        """
        return len(self.rows[0])

    def clear(self, value):
        """
        clears all items of the array to the given value
        :param value:
        :return: None
        """
        for arr in self.rows:
            arr.clear(value)

    def __getitem__(self, index_tup):
        assert len(index_tup) == 2
        row = index_tup[0]
        col = index_tup[1]
        assert 0 <= row < self.num_rows()
        assert 0 <= col < self.num_cols()
        arr_1d = self.rows[row]
        return arr_1d[col]

    def __setitem__(self, index_tup, value):
        assert len(index_tup) == 2
        row = index_tup[0]
        col = index_tup[1]
        assert 0 <= row < self.num_rows()
        assert 0 <= col < self.num_cols()
        arr_1d = self.rows[row]
        arr_1d[col] = value
