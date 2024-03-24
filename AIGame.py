from copy import deepcopy
import random
"""

AI在蒙特卡洛决策时， “模拟”步骤需要很多轮的随机走子

该类实现蒙特卡洛搜索中的“模拟”步骤

"""
class Simulate_Game:
    def __init__(self, color, board):
        self.board = board
        self.current_color = color

    #在AI之间模拟时，切换落子角色
    def switch_player(self):
        if self.current_color == 1:
            self.current_color = 2
        else:
            self.current_color = 1

    #判断当前模拟是否结束，即是否产生了赢家
    def game_over(self):
        if len(self.board.get_legal_moves(1)) == 0 and len(self.board.get_legal_moves(2)) == 0:
            return True

    #贪心策略，AI之间模拟时总是选择在使得翻转的棋子数量最多的地方落子
    def greedy_move(self):
        list = []
        moves = self.board.get_legal_moves(self.current_color)
        if moves:
            for move in moves:
                reversed = self.board.list_reversed(move, self.current_color)
                num_reversed = len(reversed)
                list.append(num_reversed)
            return moves[list.index(max(list))]

    #随机策略，AI之间模拟对弈时随机选择落子
    def random_move(self):
        moves = self.board.get_legal_moves(self.current_color)
        if moves:
            return random.choice(moves)

    #开始随机走子，直到AI之间的模拟分出胜负
    def run(self):
        while True:
            if self.game_over():
                return self.board.get_winner()
            move = self.random_move()
            if move is not None:  # 确保move不是None
                self.board.move(move, self.current_color)
            self.switch_player()





