from copy import deepcopy
from math import inf


class TreeNode:

    def __init__(self, board, player, turn, depth=0):
        self.board = deepcopy(board)
        self.depth = depth
        self.children = []
        self.value = None
        if depth > 0:
            for i in range(len(board)):
                for j in range(len(board[i])):
                    if self.board[i][j] == 0:
                        self.board[i][j] = turn
                        self.children.append(TreeNode(self.board, player, turn * -1, depth - 1))
                        self.board[i][j] = 0
        else:
            lines = create_lines(self.board, player)
            self.value = evaluate(lines, turn == player)


def blast(list_of_letters):
    new_list = []
    for s in list_of_letters:
        for i in range(len(s)):
            if s[i] == "a":
                new_string = s[:i] + " " + s[i + 1:]
                add = True
                for string in list_of_letters:
                    if new_string in string:
                        add = False
                if add:
                    new_list.append(new_string)
    return set(new_list)


d = {"aaaaa": 10 ** 100}
open_four = [" aaaa ", "a aaa a", "aa aa aa", "aaa a aaa"]
for four in open_four:
    d[four] = 10 ** 10
closed_four = blast(["aaaaa"])
for four in closed_four:
    d[four] = 10000
open_three = blast(open_four)
for three in open_three:
    d[three] = 500
closed_three = blast(closed_four)
for three in closed_three:
    d[three] = 100
open_two = blast(open_three)
for two in open_two:
    d[two] = 50
closed_two = blast(closed_three)
for two in closed_two:
    d[two] = 10
open_one = blast(open_two)
for one in open_one:
    d[one] = 5
closed_one = blast(closed_two)
for one in closed_one:
    d[one] = 1


def change_h_to_a(s):
    return s.replace("h", "a")


def create_lines(board, color):
    lines = []
    rows = len(board)
    symbols = [" ", "h", "h"]
    symbols[color] = "a"
    for i in range(rows):
        row, col, dd1, dd2, du1, du2 = "", "", "", "", "", ""
        for j in range(len(board[i])):
            row += symbols[board[i][j]]
            col += symbols[board[j][i]]
            if 0 <= i + j < rows:
                dd1 += symbols[board[i + j][j]]
                du1 += symbols[board[rows - 1 - i - j][j]]
                if i != 0:
                    dd2 += symbols[board[j][i + j]]
                    du2 += symbols[board[rows - 1 - j][i + j]]
        lines.extend((row, col, dd1, dd2, du1, du2))
    return lines


def evaluate(lines, ai_to_move):
    value = 0
    human_threat = False
    ai_threat = False
    for line in lines:
        for i in range(5, 10):
            for j in range(len(line) - i + 1):
                sub_line = line[j:i + j]
                if sub_line in d.keys():
                    value += d[sub_line]
                    if sub_line in open_three:
                        if ai_to_move:
                            value += 10 ** 10
                        elif ai_threat:
                            value += 10 ** 7
                        else:
                            ai_threat = True
                    if sub_line in closed_four:
                        if ai_to_move:
                            value += 10 ** 80
                        elif ai_threat:
                            value += 10 ** 20
                        else:
                            ai_threat = True
                if "a" not in sub_line and "h" in sub_line:
                    sub_line = change_h_to_a(sub_line)
                    if sub_line in d.keys():
                        value -= d[sub_line]
                        if sub_line in open_three:
                            if not ai_to_move:
                                value -= 10 ** 10
                            elif human_threat:
                                value -= 10 ** 7
                            else:
                                human_threat = True
                        if sub_line in closed_four:
                            if not ai_to_move:
                                value -= 10 ** 80
                            elif human_threat:
                                value -= 10 ** 20
                            else:
                                human_threat = True
    return value


class AlphaGo:

    def move(self, board, color):
        moves = {}
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 0:
                    board[i][j] = color
                    value = self.minimax(TreeNode(board, color, color * -1), False)
                    moves[(i, j)] = value
                    board[i][j] = 0
        keys = list(moves.keys())
        values = list(moves.values())
        return keys[values.index(max(values))]

    def minimax(self, tree, player, alpha=-inf, beta=inf):
        if len(tree.children) == 0:
            return tree.value
        if player:
            value = -inf
            for child in tree.children:
                newValue = self.minimax(child, False, alpha, beta)
                value = max(value, newValue)
                if value >= beta:
                    break
                alpha = max(alpha, value)
            return value
        else:
            value = inf
            for child in tree.children:
                newValue = self.minimax(child, True, alpha, beta)
                value = min(value, newValue)
                if value <= alpha:
                    break
                beta = min(beta, value)
            return value
