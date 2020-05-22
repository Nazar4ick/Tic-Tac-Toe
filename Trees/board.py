from array2d import Array2D
from linked_binary_tree import LinkedBinaryTree
import random


class Board:
    """
    Class for board representation
    """
    def __init__(self, cur_array=None):
        """
        Initializes a new Board
        """
        self.board = Array2D(3, 3)
        self.last_position = None
        self.last_symbol = None
        if cur_array is not None:
            for i in range(cur_array.num_cols()):
                for j in range(cur_array.num_rows()):
                    self.board[i, j] = cur_array[i, j]

    @staticmethod
    def check_win(game):
        """
        Checks if anybody has won yet
        :param game: object
        :return: bool
        """
        j = 0
        # check for winning rows
        for i in range(game.board.num_cols()):
            if game.board[i, j] == game.board[i, j + 1] \
                    == game.board[i, j + 2] is not None:
                if game.board[i, j] == 'o':
                    return 1
                return -1
        # check for winning columns
        for k in range(game.board.num_rows()):
            if game.board[j, k] == game.board[j + 1, k] \
                    == game.board[j + 2, k] is not None:
                if game.board[j, k] == 'o':
                    return 1
                return -1
        # check for winning diagonals
        if game.board[0, 0] == game.board[1, 1] ==\
                game.board[2, 2] is not None \
                or game.board[0, 2] == game.board[1, 1] == \
                game.board[2, 0] is not None:
            if game.board[1, 1] == 'o':
                return 1
            return -1
        return 0

    @staticmethod
    def available_positions(board):
        """
        returns all available positions of a board
        :param board: object
        :return: list
        """
        positions = []
        for i in range(board.board.num_cols()):
            for j in range(board.board.num_rows()):
                if board.board[i, j] is None:
                    positions.append((i, j))
        return positions

    def build_tree(self):
        """
        Builds the game tree
        :return: object
        """
        game_tree = LinkedBinaryTree()
        board = self.board
        game_tree._add_root(Board(board))

        def add_board(tree, node):
            """
            adds new board to a tree
            :param tree: object
            :param node: object
            :return: None
            """
            positions = self.available_positions(node._element)
            if not positions:
                return None
            if tree.height() == tree.depth(tree._make_position(node)) \
                    and tree.height() % 2 == 0:
                symbol = 'o'
            else:
                symbol = 'x'
            pos = random.choice(positions)
            new_board = Board(node._element.board)
            new_board.board[pos[0], pos[1]] = symbol
            tree._add_left(tree._make_position(node), Board(new_board.board))
            positions = self.available_positions(new_board)
            if not positions:
                return None
            pos = random.choice(positions)
            new_board = Board(node._element.board)
            new_board.board[pos[0], pos[1]] = symbol
            tree._add_right(tree._make_position(node), Board(new_board.board))
            add_board(tree, node._left)
            add_board(tree, node._right)

        add_board(game_tree, game_tree._root)
        return game_tree

    def count_wins(self):
        """
        Counts wins surplus of each branch
        :return:
        """
        tree = self.build_tree()
        node1 = tree._root._left
        node2 = tree._root._right
        wins1 = []
        wins2 = []

        def recurse_win(node, wins):
            """
            recurses through all elements of a branch
            :param node: object
            :param wins: lst
            :return: None
            """
            if node is None:
                return None
            wins.append(self.check_win(node._element))
            recurse_win(node._left, wins)
            recurse_win(node._right, wins)

        recurse_win(node1, wins1)
        recurse_win(node2, wins2)
        return sum(wins1), sum(wins2), tree

    def make_move(self):
        """
        Decides which move to make
        :return: None
        """
        all_wins = self.count_wins()
        wins1 = all_wins[0]
        wins2 = all_wins[1]
        tree = all_wins[2]
        # if wins1 >= wins2, move to the left board
        if wins1 >= wins2:
            self.board = tree._root._left._element.board
        # if wins1 < wins2, move to the right board
        else:
            self.board = tree._root._right._element.board

    def __str__(self):
        """
        draws a board
        """
        string = ''
        for i in range(self.board.num_cols()):
            for j in range(self.board.num_rows()):
                if self.board[i, j]:
                    string += self.board[i, j] + '|'
                else:
                    string += ' ' + '|'
            string = string[:-1] + '\n'
        return string
