import time
from AI import AI_Player
from ReversiBoard import Reversi

ai = AI_Player(2)


class Game:
    reversi = Reversi()
    startTime = 0
    endTime = 0
    total_time_black = 0
    total_time_white = 0

    def __init__(self):
        self.turn = True  # True为黑回合，False为白回合

    def initBoard(self):
        self.turn = True
        self.total_time_black = 0
        self.total_time_white = 0
        # for i in range(8):
        #    for j in range(8):
        #        self.Reversi.board[i][j] = "."

        # self.Reversi.board[3][3] = 1
        # self.Reversi.board[4][4] = 1
        # self.Reversi.board[3][4] = 2
        # self.Reversi.board[4][3] = 2
        self.reversi.initBoard()
        print("棋盘初始化.....")
        self.startTime = time.time()

    def get_valid_moves(self, now_turn):
        valid_moves = []
        for x in range(8):
            for y in range(8):
                if self.reversi.board[x][y] == "." and self.is_valid_move(x, y, now_turn):
                    valid_moves.append((x, y))
        return valid_moves

    def is_valid_move(self, x, y, now_turn):
        if self.reversi.board[x][y] != ".":
            return False

        directions = [(0, 1), (1, 0), (1, 1), (-1, -1), (-1, 0), (0, -1), (-1, 1), (1, -1)]
        for dx, dy in directions:
            if self.check_direction(x, y, dx, dy, now_turn):
                return True
        return False

    def check_direction(self, x, y, dx, dy, now_turn):
        opponent = 2 if now_turn else 1
        player = 1 if now_turn else 2
        x += dx
        y += dy
        if not self.is_on_board(x, y) or self.reversi.board[x][y] != opponent:
            return False

        while self.is_on_board(x, y) and self.reversi.board[x][y] == opponent:
            x += dx
            y += dy

        if not self.is_on_board(x, y):
            return False

        return self.reversi.board[x][y] == player

    def is_on_board(self, x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def game_result(self):
        # 游戏结果判断逻辑
        black_count, white_count = 0, 0
        for row in self.reversi.board:
            for cell in row:
                if cell == 1:
                    black_count += 1
                elif cell == 2:
                    white_count += 1

        if (black_count + white_count == 64
                or (len(self.get_valid_moves(self.turn)) == 0
                    and len(self.get_valid_moves(not self.turn)) == 0)):
            message = f"黑子： {black_count}   白子： {white_count}."
            print(message)
            if black_count > white_count:
                return 1  # 黑方获胜
            elif black_count < white_count:
                return 2  # 白方获胜
            else:
                return 3  # 平局
        return 0  # 游戏未结束

    def flip_pieces(self, x, y, now_turn):
        opponent = 2 if now_turn else 1
        player = 1 if now_turn else 2
        directions = [(0, 1), (1, 0), (1, 1), (-1, -1), (-1, 0), (0, -1), (-1, 1), (1, -1)]

        to_flip = []
        for dx, dy in directions:
            nx, ny = x, y
            nx += dx
            ny += dy
            flip = []
            while self.is_on_board(nx, ny) and self.reversi.board[nx][ny] == opponent:
                flip.append((nx, ny))
                nx += dx
                ny += dy

            if self.is_on_board(nx, ny) and self.reversi.board[nx][ny] == player and flip:
                to_flip.extend(flip)

        for fx, fy in to_flip:
            self.reversi.board[fx][fy] = player

    def Black(self, x, y):
        if self.game_result() == 0:
            if len(self.get_valid_moves(self.turn)) == 0:
                print("黑方无棋可下，白方继续")
                self.turn = False
                return
            if self.is_valid_move(x, y, self.turn):
                self.reversi.board[x][y] = 1
                self.endTime = time.time()
                stepTime = self.endTime - self.startTime - 0.2
                print("单步时间：", stepTime, "s")
                self.total_time_black += stepTime
                self.startTime = time.time()
                self.flip_pieces(x, y, self.turn)
                self.reversi.print_board()
                if self.game_result() == 1:
                    print("黑子获胜，游戏结束")
                    return
                elif self.game_result() == 2:
                    print("白子获胜，游戏结束")
                    return
                elif self.game_result() == 3:
                    print("平局，太离谱了")
                    return
                self.turn = False
            else:
                print("黑方位置不合法")
        elif self.game_result() == 1:
            print("黑子获胜，游戏结束")
        elif self.game_result() == 2:
            print("白子获胜，游戏结束")
        elif self.game_result() == 3:
            print("平局，太离谱了")

    def White(self, x, y):
        if self.game_result() == 0:
            if len(self.get_valid_moves(self.turn)) == 0:
                print("白方无棋可下，黑方继续")
                self.turn = True
                return
            if self.is_valid_move(x, y, self.turn):
                self.reversi.board[x][y] = 2
                self.endTime = time.time()
                stepTime = self.endTime - self.startTime - 0.2
                print("单步时间：", stepTime, "s")
                self.total_time_white += stepTime
                self.startTime = time.time()
                self.flip_pieces(x, y, self.turn)
                self.reversi.print_board()
                if self.game_result() == 1:
                    print("黑子获胜，游戏结束")
                    return
                elif self.game_result() == 2:
                    print("白子获胜，游戏结束")
                    return
                elif self.game_result() == 3:
                    print("平局，太离谱了")
                    return
                self.turn = True
            else:
                print("白方位置不合法")
        elif self.game_result() == 1:
            print("黑子获胜，游戏结束")
        elif self.game_result() == 2:
            print("白子获胜，游戏结束")
        elif self.game_result() == 3:
            print("平局，太离谱了")

    def outPutTime(self, timestring):
        minutes = int(timestring / 60)
        seconds = timestring % 60
        message = "{} 分 {:.2f} 秒".format(minutes, seconds)
        # print("{} 分钟, {:.2f} 秒".format(minutes, seconds))
        return message

    def playerchess(self, x, y):
        if self.turn:
            self.Black(x, y)
            print("黑方总用时:" + self.outPutTime(self.total_time_black))

    def chess(self, x, y):
        time.sleep(0.2)
        if self.turn:
            self.Black(x, y)
            print("黑方总用时:" + self.outPutTime(self.total_time_black))
        else:
            self.White(x,y)
            print("白方总用时:" + self.outPutTime(self.total_time_white))

    def aichess(self):
        if not self.turn:
            time.sleep(0.2)  # 保证基本可读性
            pos = ai.get_move(self.reversi)
            a, b = pos
            self.White(a, b)
            print("白方总用时:" + self.outPutTime(self.total_time_white))
