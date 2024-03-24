"""
棋盘类

包括棋盘初始化、判断落子是否合法，获取所有合法落子，执行落子等操作

"""
class Reversi():

    # 初始化8*8棋盘
    # "."代表空，1代表黑，2代表白
    def __init__(self):
        self.board = [["."] * 8 for i in range(8)]
        self.board[3][3], self.board[4][4] = 1, 1
        self.board[3][4], self.board[4][3] = 2, 2

    def initBoard(self):
        self.board = [["."] * 8 for i in range(8)]
        self.board[3][3], self.board[4][4] = 1, 1
        self.board[3][4], self.board[4][3] = 2, 2

    # 遍历棋盘，统计棋盘上黑子或白子的数量
    def count(self, color):
        return len([self.board[i][j] for i in range(8) for j in range(8) if self.board[i][j] == color])

    # 获取赢家
    # 若黑子多于白子，返回1
    # 若黑子小于白子，返回0
    # 若平局，返回0.5
    def get_winner(self):
        num_black, num_white = self.count(1), self.count(2)
        if num_black > num_white:
            return 1
        elif num_black == num_white:
            return 0.5
        else:
            return 0

    # 判断落子是否出界
    # 若没出界返回1,否则返回0
    def is_on_board(self, position):
        x, y = position
        return (0 <= x <= 7) and (0 <= y <= 7)

    # 判断落子处是否已经存在棋子
    # 若存在返回1,否则返回0
    # position是（2, 3)这种元组
    def is_existed(self, position):
        x, y = position
        return self.board[x][y] != "."

    # 获取某一落子后，所有会被翻转的棋子坐标
    # reversed是坐标的列表
    def list_reversed(self, position, color):
        if not self.is_on_board(position) or self.is_existed(position):
            return False
        reversed_list = []
        op_color = 1 if color == 2 else 2  # op_color是对手的棋子颜色
        for xd, yd in [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]:
            temp = []
            x, y = position
            x += xd
            y += yd
            while self.is_on_board((x, y)) and self.board[x][y] == op_color:
                temp.append((x, y))
                x += xd
                y += yd
            if self.is_on_board((x, y)) and self.board[x][y] == color:
                reversed_list += temp
        return reversed_list

    # 判断当前落子坐标是否合法
    # 若合法返回1，否则返回0
    def is_legal_move(self, position, color):
        return self.list_reversed(position, color)

    # 获取黑子或白字当前所有的合法落子坐标
    # 返回一个坐标列表
    def get_legal_moves(self, color):
        return [(x, y) for x in range(8) for y in range(8) if self.is_legal_move((x, y), color)]

    # 执行落子操作
    def move(self, position, color):
        if self.is_legal_move(position, color):
            reversed_list = self.list_reversed(position, color)
            if reversed:
                x, y = position
                self.board[x][y] = color
                for x, y in reversed_list:
                    self.board[x][y] = color
            return True
        else:
            return False

    # 打印棋盘
    def print_board(self):
        print("", end="   ")
        for i in range(8):
            print(i, end="    ")
        print("\n")
        for x in range(8):
            print(x, end="  ")
            for y in range(8):
                print(self.board[x][y], end="    ")
            print("\n")
        print("----------分割线----------")

