import copy


class GameState:
    def __init__(self, values, states, play):
        self.board = states
        self.values = values
        self.player = play
        if play == 'X':
            self.opponent = 'O'
        else:
            self.opponent = 'X'

    def get_score(self):
        score_player, score_opponent = 0, 0
        for i in range(dim):
            for j in range(dim):
                if self.board[i][j] == self.player:
                    score_player += int(self.values[i][j])
                elif self.board[i][j] == self.opponent:
                    score_opponent += int(self.values[i][j])
        return score_player - score_opponent

    def get_legal_moves(self, whose_turn):
        legal_moves, legal_raids = [], []
        for i in range(dim):
            for j in range(dim):
                if self.board[i][j] == '.':
                    legal_moves.append((i, j, 'Stake'))
                    if self.check_raid((i, j), whose_turn):
                        legal_raids.append((i, j, 'Raid'))
        legal_moves.extend(legal_raids)
        if not legal_moves:
            legal_moves = [None]
        return legal_moves

    def check_raid(self, move, whose_turn):
        i, j = move[0], move[1]
        if whose_turn == self.player:
            opponent = self.opponent
        else:
            opponent = self.player
        condition_1, condition_2 = False, False
        if dim - 1 >= i - 1 >= 0 and self.board[i - 1][j] == opponent:
            condition_1 = True
        if dim - 1 >= i + 1 >= 0 and self.board[i + 1][j] == opponent:
            condition_1 = True
        if dim - 1 >= j - 1 >= 0 and self.board[i][j - 1] == opponent:
            condition_1 = True
        if dim - 1 >= j + 1 >= 0 and self.board[i][j + 1] == opponent:
            condition_1 = True
        if dim - 1 >= i - 1 >= 0 and self.board[i - 1][j] == whose_turn:
            condition_2 = True
        if dim - 1 >= i + 1 >= 0 and self.board[i + 1][j] == whose_turn:
            condition_2 = True
        if dim - 1 >= j - 1 >= 0 and self.board[i][j - 1] == whose_turn:
            condition_2 = True
        if dim - 1 >= j + 1 >= 0 and self.board[i][j + 1] == whose_turn:
            condition_2 = True
        if condition_1 and condition_2:
            return True
        else:
            return False

    def make_move(self, move, whose_turn):
        i, j, m_type = move[0], move[1], move[2]
        self.board[i][j] = whose_turn
        if m_type == 'Raid':
            self.raid_move(move, whose_turn)

    def raid_move(self, move, whose_turn):
        i, j = move[0], move[1]
        if whose_turn == self.player:
            opponent = self.opponent
        else:
            opponent = self.player
        if dim - 1 >= i - 1 >= 0 and self.board[i - 1][j] == opponent:
            self.board[i - 1][j] = whose_turn
        if dim - 1 >= i + 1 >= 0 and self.board[i + 1][j] == opponent:
            self.board[i + 1][j] = whose_turn
        if dim - 1 >= j - 1 >= 0 and self.board[i][j - 1] == opponent:
            self.board[i][j - 1] = whose_turn
        if dim - 1 >= j + 1 >= 0 and self.board[i][j + 1] == opponent:
            self.board[i][j + 1] = whose_turn

    def game_over(self):
        for i in range(0, dim):
            for j in range(0, dim):
                if self.board[i][j] == '.':
                    return False
        return True


class Move:
    def __init__(self, flag):
        if flag == '+':
            self.score = float('inf')
        elif flag == '-':
            self.score = - float('inf')
        self.move = (0, 0)
        self.game_state = game
        self.move_type = ''

    def get_score(self):
        return self.score

    def get_move(self):
        return self.move

    def get_game_state(self):
        return self.game_state

    def get_type(self):
        return self.move_type

    def set_score(self, value):
        self.score = value

    def set_move(self, values):
        self.move = values

    def set_game_state(self, game_state):
        self.game_state = game_state

    def set_type(self, value):
        self.move_type = value


def func_switch_turn(who):
    if who == 'X':
        return 'O'
    else:
        return 'X'


def func_is_empty_file():
    try:
        file_obj = open(file_name)
        input_d = ''
        try:
            input_d = file_obj.read()
        finally:
            file_obj.close()
            return input_d == ''
    except IOError:
        print('The file does not exist.')


def func_write_file(output_data):
    try:
        file_obj = open('output.txt', 'w')
        try:
            file_obj.write(output_data)
        finally:
            file_obj.close()
    except IOError:
        print('Cannot write the output data into file.')


def func_print_file_content(file_name):
    try:
        file_obj = open(file_name)
        try:
            print(file_obj.read())
        finally:
            file_obj.close()
    except IOError:
        print('The file does not exist.')


def func_get_line_from_file(file_obj, desired_line):
    if desired_line < 1:
        return ''
    for curr_line, line in enumerate(file_obj):
        if curr_line == desired_line - 1:
            return line
    return ''


def func_create_table(file_obj, line_count):
    tab_list = list([])
    for i in range(0, line_count):
        tab_list.append(str.split(func_get_line_from_file(file_obj, 1)))
    return tab_list


def func_create_state(file_obj, dimension):
    states = list([])
    for i in range(0, dimension):
        states.append(list(str.split(func_get_line_from_file(file_obj, 1))[0]))
    return states


def func_max_eval(game_inst, current_depth, whose_turn):
    if current_depth == 0 or game_inst.game_over():
        return game_inst.get_score()
    best_move = Move('-')
    for move in game_inst.get_legal_moves(whose_turn):
        g_copy = copy.deepcopy(game_inst)
        g_copy.make_move(move, whose_turn)
        move_eval = func_min_eval(g_copy, current_depth - 1, func_switch_turn(whose_turn))
        move_type = move[2]
        if move_eval > best_move.get_score():
            best_move.set_score(move_eval)
            best_move.set_type(move_type)
        elif move_eval == best_move.get_score():
            if best_move.get_type() == 'Raid' and move_type == 'Stake':
                best_move.set_score(move_eval)
                best_move.set_type(move_type)
        del g_copy
    return best_move.get_score()


def func_min_eval(game_inst, current_depth, whose_turn):
    if current_depth == 0 or game_inst.game_over():
        return game_inst.get_score()
    best_move = Move('+')
    for move in game_inst.get_legal_moves(whose_turn):
        g_copy = copy.deepcopy(game_inst)
        g_copy.make_move(move, whose_turn)
        move_type = move[2]
        move_eval = func_max_eval(g_copy, current_depth - 1, func_switch_turn(whose_turn))
        if move_eval < best_move.get_score():
            best_move.set_score(move_eval)
            best_move.set_type(move_type)
        elif move_eval == best_move.get_score():
            if best_move.get_type() == 'Raid' and move_type == 'Stake':
                best_move.set_score(move_eval)
                best_move.set_type(move_type)
        del g_copy
    return best_move.get_score()


def func_minimax():
    next_move = Move('-')
    for move in game.get_legal_moves(game.player):
        game_copy = copy.deepcopy(game)
        game_copy.make_move(move, game_copy.player)
        move_value = func_min_eval(game_copy, maxdepth - 1, game.opponent)
        move_type = move[2]
        if move_value > next_move.get_score():
            next_move.set_score(move_value)
            next_move.set_move(move)
            next_move.set_type(move_type)
            next_move.set_game_state(game_copy.board)
        elif move_value == next_move.get_score():
            if next_move.get_type() == 'Raid' and move_type == 'Stake':
                next_move.set_score(move_value)
                next_move.set_move(move)
                next_move.set_type(move_type)
                next_move.set_game_state(game_copy.board)
        del game_copy
    return next_move


def func_max_alphabeta_eval(game_inst, current_depth, whose_turn, alpha, beta):
    if current_depth == 0 or game_inst.game_over():
        return game_inst.get_score()
    for move in game_inst.get_legal_moves(whose_turn):
        g_copy = copy.deepcopy(game_inst)
        g_copy.make_move(move, whose_turn)
        move_eval = func_min_alphabeta_eval(g_copy, current_depth - 1, func_switch_turn(whose_turn), alpha, beta)
        if move_eval >= beta:
            return move_eval
        if move_eval > alpha:
            alpha = move_eval
        del g_copy
    return alpha


def func_min_alphabeta_eval(game_inst, current_depth, whose_turn, alpha, beta):
    if current_depth == 0 or game_inst.game_over():
        return game_inst.get_score()
    for move in game_inst.get_legal_moves(whose_turn):
        g_copy = copy.deepcopy(game_inst)
        g_copy.make_move(move, whose_turn)
        move_eval = func_max_alphabeta_eval(g_copy, current_depth - 1, func_switch_turn(whose_turn), alpha, beta)
        if move_eval <= alpha:
            return move_eval
        if move_eval < beta:
            beta = move_eval
        del g_copy
    return beta


def func_alphabeta():
    next_move = Move('-')
    alpha, beta = - float('inf'), float('inf')
    for move in game.get_legal_moves(game.player):
        game_copy = copy.deepcopy(game)
        game_copy.make_move(move, game_copy.player)
        move_value = func_min_alphabeta_eval(game_copy, maxdepth - 1, game.opponent, alpha, beta)
        move_type = move[2]
        if move_value > next_move.get_score():
            next_move.set_score(move_value)
            next_move.set_move(move)
            next_move.set_type(move_type)
            next_move.set_game_state(game_copy.board)
        elif move_value == next_move.get_score():
            if next_move.get_type() == 'Raid' and move_type == 'Stake':
                next_move.set_score(move_value)
                next_move.set_move(move)
                next_move.set_type(move_type)
                next_move.set_game_state(game_copy.board)
        del game_copy
    return next_move


def func_competition():
    return ''


def func_print_game_state(g_state):
    print_str = ''
    for i in range(0, dim):
        for j in range(0, dim):
            print_str += g_state[i][j]
        print_str += '\n'
    return print_str


file_name = 'input.txt'
s_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
if not func_is_empty_file():
    # func_print_file_content(file_name)
    file_inst = open(file_name, 'rU')
    dim = int(func_get_line_from_file(file_inst, 1).rstrip())
    mode = func_get_line_from_file(file_inst, 1).rstrip()
    my_play = func_get_line_from_file(file_inst, 1).rstrip()
    maxdepth = int(func_get_line_from_file(file_inst, 1).rstrip())
    table = func_create_table(file_inst, dim)
    state = func_create_state(file_inst, dim)
    game = GameState(table, state, my_play)
    output_data = ''
    if mode == 'MINIMAX':
        data = func_minimax()
        output_data = s_alphabet[data.get_move()[1]] + str(
            data.get_move()[0] + 1) + ' ' + data.get_type() + '\n' + func_print_game_state(data.get_game_state())
    elif mode == 'ALPHABETA':
        alpha, beta = - float('inf'), float('inf')
        data = func_alphabeta()
        output_data = s_alphabet[data.get_move()[1]] + str(
            data.get_move()[0] + 1) + ' ' + data.get_type() + '\n' + func_print_game_state(data.get_game_state())
    elif mode == 'COMPETITION':
        output_data = func_minimax()
    else:
        print('The mode in the input file is incorrect.')
    if output_data != '':
        func_write_file(output_data)
        # func_print_file_content('output.txt')
else:
    print('Something went wrong. Either the file is corrupted or it does not exist.')
