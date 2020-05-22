from board import Board


def main():
    """
    Controls the flow of the game
    """
    game_board = Board()
    while True:
        try:
            row = int(input('In which row would you like to place '
                            'x (write a number starting from 1): '))

            col = int(input('In which column would you like to '
                            'place x (write a number starting from 1): '))
            if game_board.board[row - 1, col - 1]:
                raise ValueError
            game_board.board[row - 1, col - 1] = 'x'
            print(game_board)
            if game_board.check_win(game_board):
                if game_board.check_win(game_board) == -1:
                    print('Congratulations, you won!')
                else:
                    print('Oh no, you lost :(')
                break
            # if no more spots left, break
            elif not game_board.available_positions(game_board):
                print('It is a tie')
                break
            game_board.make_move()
            print(game_board)
        except ValueError:
            print('Incorrect row or col, try again')
        except AssertionError:
            print('Incorrect row or col, try again')


main()
