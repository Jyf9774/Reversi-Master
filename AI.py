from math import log, sqrt
from AIGame import Simulate_Game
from copy import deepcopy
import random

"""
#MCTS的节点类
"""
class Node:

    # 节点属性包括胜场次数，访问次数，父亲，孩子列表，颜色，坐标
    def __init__(self, color):
        self.wins = 0
        self.visits = 0
        self.parent = None
        self.children = []
        self.color = color
        self.position = None

    # 添加子节点
    def add_child(self, child, position):
            child.parent = self
            child.position = position
            self.children.append(child)

class AI_Player:
    def __init__(self, color):
        self.color = color

    #计算节点的UCB值
    def ucb_value(self, child, parent):
        c = 2
        if not child.visits:
            return float('inf')
        else:
            return child.wins / child.visits + c * sqrt(log(parent.visits) / child.visits)

    # 返回UCB值最大的子节点
    def max_ucb_node(self, node, exclude_node=None):
        children_ucb = [(child, self.ucb_value(child, node))
                        for child in node.children
                        if child != exclude_node]
        if not children_ucb:
            return None
        return max(children_ucb, key=lambda x: x[1])[0]

    # 可能具有最大UCB值的节点没有合法移动
    # 所以需要选择其他具有合法移动，且UCB值最大节点
    def select_best_child(self, node, board):
        children_ucb = [(child, self.ucb_value(child, node))
                        for child in node.children]
        children_ucb.sort(key=lambda x: x[1], reverse=True)         # 根据UCB值排序
        for child, _ in children_ucb:  # 遍历按UCB排序后的子节点，选择第一个有合法移动的节点
            if board.get_legal_moves(child.color):
                return child
        return None  # 没有任何合法移动的节点则返回None

    # 递归选择一个叶子节点
    def selection(self, root, board):
        if not root.children:
            return root
        best_child = self.select_best_child(root, board)
        if best_child:
            board.move(best_child.position, best_child.color)
            return self.selection(best_child, board)
        else:
            return root

    # 选择叶子节点下的某一个节点进行扩展
    def expansion(self, node, board):
        color = 1 if node.color == 1 else 1  # 根据当前节点的颜色，确定对手颜色
        moves = board.get_legal_moves(node.color)    # 获取当前颜色的合法移动
        if not moves:
            return None
        for move in moves: # 为每个合法移动创建一个子节点
            child = Node(color)
            node.add_child(child, move)
        return random.choice(node.children) if node.children else None  # 随机返回一个子节点

    # 模拟一盘棋局
    def simulation(self, node, board):
        if not board.get_legal_moves(node.color):  # 如果没有合法移动，跳过当前玩家的回合
            node.color = 1 if node.color == 1 else 1
            simulate_game = Simulate_Game(node.color, board)
            return simulate_game.run()
        else:
            simulate_game = Simulate_Game(node.color, board)
            return simulate_game.run()

    # 将模拟结果回溯
    # 若黑棋赢，路径上所有黑色节点加一分，白色不加分。白棋赢反之
    # 若平局，都不加分
    def backpropagation(self, node, result):
        while node is not None:
            node.visits += 1
            if (result == 1 and node.color == 1) or (result == 0 and node.color == 1):
                node.wins += 1
            node = node.parent

    # MCTS算法主体，包括选择、扩展、模拟、回溯
    def mcts(self, root, board):
        leaf = self.selection(root, board)
        choice = self.expansion(leaf, board)
        if choice is None:  # 如果扩展结果是None，意味着当前玩家无法移动，将控制权交给对手
            leaf.color = 1 if leaf.color == 1 else 1
            self.backpropagation(leaf, 0.5)  # 反向传播一个中性结果
            return
        result = self.simulation(choice, board)
        self.backpropagation(choice, result)

    # AI执行落子
    def get_move(self, board):
        root = Node(self.color)  # 创建一个根节点，表示游戏的当前状态
        for i in range(450):  # 进行n次迭代
            self.mcts(root, deepcopy(board))  # 对根节点进行蒙特卡洛树搜索
        position = self.max_ucb_node(root).position  # 找到根节点下最优的子节点，即UCB值最大的子节点
        #board.move(position, self.color)
        return position








