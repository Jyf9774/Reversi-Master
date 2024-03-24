import sys
import threading
import time

from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPen
from PyQt5.QtCore import Qt
from game import Game

gameMode = ""
class ChessboardWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.gameMode = gameMode


    def initUI(self):
        self.setGeometry(800, 400, 800, 800)
        self.setWindowTitle('Reversi Master')

    def popup(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Reversi Master")
        msg.setText("选择对手")
        msg.addButton("人", QMessageBox.ActionRole)
        msg.addButton("AI", QMessageBox.ActionRole)
        retval = msg.exec_()
        print(retval)
        if retval == 1:
            print("AI clicked.")
            self.gameMode = "AI"

        elif retval == 0:
            print("Person clicked.")
            self.gameMode = "Person"

    def aimove(self):
        g.aichess()


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.black)
        pen.setWidth(3)
        painter.setPen(pen)
        width = self.width()
        height = self.height()
        cell_width = width // 8
        cell_height = width // 8
        pixmap = QPixmap('chessboard.jpg')
        painter.drawPixmap(0, 0, width, height, pixmap)
        for i in range(8):
            for j in range(8):
                painter.drawRect(i * cell_width, j * cell_height, cell_width, cell_height)
        painter.end()
        for i in range(8):
            for j in range(8):
                if Game.reversi.board[i][j] == 1:
                    self.drawChessPiece(i, j, True)
                elif Game.reversi.board[i][j] == 2:
                    self.drawChessPiece(i, j, False)
        self.raise_()

    def drawChessPiece(self, x, y, isBlack):
        width = self.width()
        height = self.height()
        cell_width = width // 8
        cell_height = height // 8

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        # 设置棋子的颜色
        if isBlack:
            color = QColor(0, 0, 0)  # 黑色棋子
        else:
            color = QColor(255, 255, 255)  # 黑色棋子
        painter.setBrush(color)

        # 绘制棋子
        diameter = int(cell_width * 8 / 10)
        painter.drawEllipse(x * cell_width + int(cell_width / 9), y * cell_height + int(cell_height / 9), diameter,
                            diameter)
        self.raise_()
        painter.end()

    def mousePressEvent(self, event):
        print("mousePressEvent")
        if event.button() == Qt.LeftButton:
            mouse_x = event.windowPos().x()
            mouse_y = event.windowPos().y()
            print("mouse_x,y", mouse_x, mouse_y)
            print(self.width(), self.height())
            cell_width = self.width() // 8
            cell_height = self.height() // 8
            game_x = int(mouse_x // cell_width)
            game_y = int(mouse_y // cell_height)
            print("点击坐标：x=", game_x + 1, "y=", game_y + 1)
            if self.gameMode == "AI":
                try:
                    time.sleep(0.2)     #延迟落子，防止误触
                    g.playerchess(game_x, game_y)
                except Exception as e:
                    print(e)
                self.repaint(0, 0, self.width(), self.height())
                super(ChessboardWindow, self).mousePressEvent(event)
                self.setEnabled(False)
                self.aimove()
                self.repaint(0, 0, self.width(), self.height())
                self.setEnabled(True)
            elif self.gameMode == "Person":
                g.chess(game_x, game_y)
                self.repaint(0, 0, self.width(), self.height())

        self.repaint(0, 0, self.width(), self.height())

        timeBlack = g.outPutTime(g.total_time_black)
        timeWhite = g.outPutTime(g.total_time_white)
        message = "\n黑方用时：" + timeBlack + "\n白方用时：" + timeWhite
        if g.game_result() == 1:
            QMessageBox.about(self, '游戏结束', '黑子获胜!\n总用时为' + message)
            g.initBoard()
            self.popup()
        elif g.game_result() == 2:
            QMessageBox.about(self, '游戏结束', '白子获胜!\n总用时为' + message)
            g.initBoard()
            self.popup()
        elif g.game_result() == 3:
            QMessageBox.about(self, '游戏结束', '平局，太离谱了\n总用时为' + message)
            g.initBoard()
            self.popup()


if __name__ == '__main__':
    g = Game()
    app = QApplication(sys.argv)

    window = ChessboardWindow()
    window.setFixedSize(1000, 1000)
    window.show()
    window.popup()
    g.initBoard()
    g.reversi.print_board()
    sys.exit(app.exec_())
