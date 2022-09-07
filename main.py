'''
Author: Solomon Asad  Last modified: Aug. 30, 2022
'''

def is_empty(board):
    '''
        Returns True if and only if there are no stones on the board 'board'.
        Parameters:
            board : list of lists
    '''

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == "w" or board[i][j] == "b":
                return False
    return True

def is_off_board(board, x, y): #checks if x, y coord is off board
    if x < 0 or x >= 8 or y < 0 or y >= 8:
        return True
    return False

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    '''
        Check the ends of sequences. Is there a square there, and is it empty?
        If only one square and empty return Semi-Open
        If two squares and empty return Open
        If no squares/1 square/2 square but not empty return Closed
        Hint: Bunch of If statements
    '''
    begin_closed = False
    end_closed = False

    # Finding the coordinate of before/end of sequence
    x_begin_m1 = x_end - (length * d_x)
    y_begin_m1 = y_end - (length * d_y)

    x_end_p1 = x_end + 1 * d_x
    y_end_p1 = y_end + 1 * d_y

    off_board_begin = is_off_board(board, x_begin_m1, y_begin_m1)
    off_board_end = is_off_board(board, x_end_p1, y_end_p1)

    if (off_board_begin == True) or (board[y_begin_m1][x_begin_m1]) != " ":
        begin_closed = True

    if (off_board_end == True) or (board[y_end_p1][x_end_p1]) != " ":
        end_closed = True

    if begin_closed and end_closed:
        return "CLOSED"
    elif begin_closed or end_closed:
        return "SEMIOPEN"
    else:
        return "OPEN"

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    '''
    Analysez sequence of squares adjacent either horiz, vert, or diag
    Return tuple where first element = # of open sequences of col of length in the row
    Second element = # of semi-open sequences of col of length in the row
    '''
    counter_sequence = 0
    counter_iteration = 1
    counter_stones = 0

    open_seq_count = 0
    semi_open_seq_count = 0

    x_start2 = x_start
    y_start2 = y_start

    while not is_off_board(board, x_start, y_start):
    #while 0 <= y_start < len(board) and 0 <= x_start < len(board): # stays inside board
        y_start += d_y
        x_start += d_x
        counter_sequence += 1

    while counter_iteration <= counter_sequence:
        if board[y_start2][x_start2] == col:
            counter_stones += 1
        else:
            counter_stones = 0

        if (is_off_board(board, x_start2 + d_x, y_start2 + d_y) or (board[y_start2 + d_y][x_start2 + d_x] != col)) and (counter_stones == length):
            if is_bounded(board, y_start2, x_start2, length, d_y, d_x) == "OPEN":
                open_seq_count += 1
            elif is_bounded(board, y_start2, x_start2, length, d_y, d_x) == "SEMIOPEN":
                semi_open_seq_count += 1

        counter_iteration += 1
        y_start2 += d_y
        x_start2 += d_x

    return open_seq_count, semi_open_seq_count

def detect_row_closed(board, col, y_start, x_start, length, d_y, d_x):
    counter_sequence = 0
    counter_iteration = 1
    counter_stones = 0

    open_seq_count = 0
    semi_open_seq_count = 0
    closed_seq_count = 0

    x_start2 = x_start
    y_start2 = y_start

    while not is_off_board(board, x_start, y_start):
    #while 0 <= y_start < len(board) and 0 <= x_start < len(board): # stays inside board
        y_start += d_y
        x_start += d_x
        counter_sequence += 1

    while counter_iteration <= counter_sequence:
        if board[y_start2][x_start2] == col:
            counter_stones += 1
        else:
            counter_stones = 0

        if (is_off_board(board, x_start2 + d_x, y_start2 + d_y) or (board[y_start2 + d_y][x_start2 + d_x] != col)) and (counter_stones == length):
            if is_bounded(board, y_start2, x_start2, length, d_y, d_x) == "OPEN":
                open_seq_count += 1
            elif is_bounded(board, y_start2, x_start2, length, d_y, d_x) == "SEMIOPEN":
                semi_open_seq_count += 1

            elif is_bounded(board, y_start2, x_start2, length, d_y, d_x) == "CLOSED":
                closed_seq_count += 1

        counter_iteration += 1
        y_start2 += d_y
        x_start2 += d_x

    return open_seq_count, semi_open_seq_count, closed_seq_count

def detect_rows(board, col, length):
    ''' This function analyses the board board. The function returns a tuple, whose first element is the
number of open sequences of colour col of length length on the entire board, and whose second
element is the number of semi-open sequences of colour col of length length on the entire board
    '''
    open_seq_count, semi_open_seq_count = 0, 0
    #i, j, k, l, m, n
    i = 0
    k = 0

    for j in range(len(board)):
        row_result = detect_row(board, col, i, j, length, 1, 0) # Vert, since i is 0
        open_seq_count += row_result[0]
        semi_open_seq_count += row_result[1]

        row_result = detect_row(board, col, i, j, length, 1, -1) # Top R to Bottom L
        open_seq_count += row_result[0]
        semi_open_seq_count += row_result[1]

        row_result = detect_row(board, col, j, i, length, 0, 1) # Horiz
        open_seq_count += row_result[0]
        semi_open_seq_count += row_result[1]

        if j == 7:
            for m in range(1, len(board)):
                row_result = detect_row(board, col, m, j, length, 1, -1) # Top R to Bottom L
                open_seq_count += row_result[0]
                semi_open_seq_count += row_result[1]

        row_result = detect_row(board, col, j, i, length, 1, 1)
        open_seq_count += row_result[0]
        semi_open_seq_count += row_result[1]

        if j == 0:
            for n in range(1, len(board)):
                row_result = detect_row(board, col, j, n, length, 1, 1) # Top L to Bottom R
                open_seq_count += row_result[0]
                semi_open_seq_count += row_result[1]

    return open_seq_count, semi_open_seq_count

def detect_rows_closed(board, col, length):
    open_seq_count, semi_open_seq_count, closed_seq_count = 0, 0, 0
    #i, j, k, l, m, n
    i = 0
    k = 0

    for j in range(len(board)):
        row_result = detect_row_closed(board, col, i, j, length, 1, 0) # Vert, since i is 0
        open_seq_count += row_result[0]
        semi_open_seq_count += row_result[1]
        closed_seq_count += row_result[2]

        row_result = detect_row_closed(board, col, i, j, length, 1, -1) # Top R to Bottom L
        open_seq_count += row_result[0]
        semi_open_seq_count += row_result[1]
        closed_seq_count += row_result[2]

        row_result = detect_row_closed(board, col, j, i, length, 0, 1) # Horiz
        open_seq_count += row_result[0]
        semi_open_seq_count += row_result[1]
        closed_seq_count += row_result[2]

        if j == 7:
            for m in range(1, len(board)):
                row_result = detect_row_closed(board, col, m, j, length, 1, -1) # Top R to Bottom L
                open_seq_count += row_result[0]
                semi_open_seq_count += row_result[1]
                closed_seq_count += row_result[2]

        row_result = detect_row_closed(board, col, j, i, length, 1, 1)
        open_seq_count += row_result[0]
        semi_open_seq_count += row_result[1]
        closed_seq_count += row_result[2]

        if j == 0:
            for n in range(1, len(board)):
                row_result = detect_row_closed(board, col, j, n, length, 1, 1) # Top L to Bottom R
                open_seq_count += row_result[0]
                semi_open_seq_count += row_result[1]
                closed_seq_count += row_result[2]

    return open_seq_count, semi_open_seq_count, closed_seq_count


def search_max(board):
    '''
    - iterate through board, place 'b', run score, place score into a counter. Do loop again check if the score is now greater than the old score. If true replace that score with the new score.
    '''
    temporary_score = -999999999999
    # make number low

    temporary_board = board
    move_y = 0
    move_x = 0
    empty_found = False

    for i in range(len(temporary_board)): # iterating through board
        for j in range(len(temporary_board)): # iterating through board

            if temporary_board[i][j] == ' ':
                if not empty_found:
                    move_y, move_x = i, j
                    empty_found = True
                temporary_board[i][j] = 'b'

                if (score(temporary_board) >= temporary_score):
                    move_y = i
                    move_x = j
                    temporary_score = score(temporary_board)
                temporary_board[i][j] = ' '

    return move_y, move_x

def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)

    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])

def is_win(board):
    '''
    Determing status of game. Returns ["White won", "Black won", "Draw", "Continue playing"]
    '''
    #Checking for win
    if detect_rows(board, 'w', 5)[0] != 0 or detect_rows(board, 'w', 5)[1] !=  0 or detect_rows_closed(board, 'w', 5)[2] != 0:
        return "White won"

    if detect_rows(board, 'b', 5)[0] != 0 or detect_rows(board, 'b', 5)[1] != 0 or detect_rows_closed(board, 'b', 5)[2] != 0:
        return "Black won"

    #Checking for Draw or Continue playing
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == " ":
                return "Continue playing"
    return 'Draw'

def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)

def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board

def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))

def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res
        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res

def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x

def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")

def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0



#
if __name__ == '__main__':
    play_gomoku(8)
#
