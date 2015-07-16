import statistics
import random
import sys
from itertools import chain

from pos import *
from datetime import datetime
from move import Move
from game_state import GameState

class BombmanAi:
    NSIMULATIONS = 5
    DEPTH = 15
    DIR = ['UP', 'DOWN', 'LEFT', 'RIGHT', 'STAY']

    def __init__(self, name, id):
        self.name = name
        self.id = id

    # 手を決定する
    # GameState → Move
    def move(self, state):
        if not state.find_player(self.id)['isAlive']:
            return Move('STAY', False)

        time_start = datetime.now()
        while True:
            moves = self.legal_moves(state, self.id)
            scores = list(map(lambda m: self.score_move(m, state), moves))
            # 生き残る未来が見えない場合は、450ms で探索を打ち切って
            # 爆弾を置かないランダムな手を選択する。
            if scores[0] < -50 and \
                all(map(lambda s: s == scores[0], scores)):
                if (datetime.now() - time_start).total_seconds() < 0.45:
                    continue
                else:
                    return [m for m in moves if not m.bomb][0]
            # 他より良い手が見付かればそれを選択する。
            return max(zip(moves, scores), key = lambda p: p[1])[0]

    # (GameState, Integer) → GameState
    # depth 手先まで、全てのプレーヤーをランダム移動させる
    # state を破壊的に変更し、state を返す
    def simulate_unsafe(self, state, depth):
        for i in range(depth):
            if not state.find_player(self.id)['isAlive']:
                break
            commands = [(id, random.choice(self.legal_moves(state, id))) for id in range(0, 4)]
            state.transition_unsafe(commands)
        return state

    # Move → Float
    # move: 手
    # state: 手を打つ直前の状態
    def score_move(self, move, state):
        def build_commands():
            commands = []
            for id in range(4):
                if id == self.id:
                    commands.append((id, move))
                else:
                    commands.append((id, random.choice(self.legal_moves(state, id))))
            return commands
            
        return statistics.mean([self.score(self.simulate_unsafe(state.transition(build_commands()), BombmanAi.DEPTH - 1), self.id)
                                for i in range(BombmanAi.NSIMULATIONS)])

    # (GameState, Integer) → [Move]
    def legal_moves(self, state, id):
        player = state.find_player(id)
        dirs = [d for d in BombmanAi.DIR
                  if d == 'STAY' or \
                     state.isenterable(addvec(player['pos'], GameState.DIR_OFFSETS[d]))]
        can_set_bomb = state.player_can_set_bomb(player)
        return list(chain(*map(lambda d: [Move(d, True), Move(d, False)] if can_set_bomb else [Move(d, False)], dirs)))

    # 評価関数
    # ゲーム状態 state はプレーヤー id にとってどれほど有利であるか
    def score(self, state, id):
        return 0 if state.find_player(id)['isAlive'] else -100
