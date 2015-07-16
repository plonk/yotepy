import copy
import json
import random
from itertools import chain

from pos import *

# テストデータ
# よてぱいの id は 1。
#
#   Turn 0
#   ■■■■■■■■■■■■■■■
#   ■予　□□□　　　□　□　発■
#   ■　■□■　■□■　■□■　■
#   ■　□□□□　□　□　□□□■
#   ■□■□■　■□■□■□■□■
#   ■　□□□□□　□　□　□□■
#   ■　■　■□■□■□■□■□■
#   ■□□□□□□□□□□□□　■
#   ■□■□■　■□■□■　■□■
#   ■□　□　□□　□□□□□□■
#   ■□■□■□■□■□■□■　■
#   ■□□□□□□□　□　□　□■
#   ■　■　■□■□■　■　■　■
#   ■よ　□□□□□□□□　　発■
#   ■■■■■■■■■■■■■■■
#

TEST_DATA = json.loads('{"turn":0,"walls":[[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[0,8],[0,9],[0,10],[0,11],[0,12],[0,13],[0,14],[1,0],[1,14],[2,0],[2,2],[2,4],[2,6],[2,8],[2,10],[2,12],[2,14],[3,0],[3,14],[4,0],[4,2],[4,4],[4,6],[4,8],[4,10],[4,12],[4,14],[5,0],[5,14],[6,0],[6,2],[6,4],[6,6],[6,8],[6,10],[6,12],[6,14],[7,0],[7,14],[8,0],[8,2],[8,4],[8,6],[8,8],[8,10],[8,12],[8,14],[9,0],[9,14],[10,0],[10,2],[10,4],[10,6],[10,8],[10,10],[10,12],[10,14],[11,0],[11,14],[12,0],[12,2],[12,4],[12,6],[12,8],[12,10],[12,12],[12,14],[13,0],[13,14],[14,0],[14,1],[14,2],[14,3],[14,4],[14,5],[14,6],[14,7],[14,8],[14,9],[14,10],[14,11],[14,12],[14,13],[14,14]],"blocks":[[2,7],[12,5],[7,7],[8,5],[6,13],[3,10],[9,9],[9,11],[4,3],[7,8],[8,13],[11,6],[12,3],[5,10],[13,5],[1,9],[13,8],[7,3],[6,5],[5,11],[7,2],[3,8],[13,9],[3,11],[9,6],[11,11],[4,1],[3,5],[8,9],[10,5],[11,4],[3,4],[10,9],[5,7],[5,6],[13,4],[3,3],[11,9],[9,13],[9,10],[2,11],[7,6],[11,3],[2,3],[1,4],[7,12],[3,9],[3,13],[1,7],[8,7],[6,9],[12,7],[2,5],[3,7],[6,7],[1,10],[5,5],[6,11],[13,3],[4,5],[1,11],[5,3],[9,1],[9,7],[7,4],[10,7],[13,11],[4,11],[5,12],[12,9],[4,13],[9,3],[7,11],[13,6],[5,1],[11,2],[5,9],[10,13],[7,10],[11,10],[5,13],[4,7],[11,7],[3,2],[9,8],[1,8],[11,1],[3,1],[7,13],[9,4]],"players":[{"name":"予定地AI","pos":{"x":1,"y":1},"power":2,"setBombLimit":2,"ch":"予","isAlive":true,"setBombCount":0,"totalSetBombCount":0,"id":0},{"name":"よてぱい","pos":{"x":1,"y":13},"power":2,"setBombLimit":2,"ch":"よ","isAlive":true,"setBombCount":0,"totalSetBombCount":0,"id":1},{"name":"発","pos":{"x":13,"y":1},"power":2,"setBombLimit":2,"ch":"発","isAlive":true,"setBombCount":0,"totalSetBombCount":0,"id":2},{"name":"発","pos":{"x":13,"y":13},"power":2,"setBombLimit":2,"ch":"発","isAlive":true,"setBombCount":0,"totalSetBombCount":0,"id":3}],"bombs":[],"items":[],"fires":[]}')

def spiral(left, right, top, bottom):
    """螺旋状の壁振り座標系列

    >>> list(spiral(1, 13, 1, 13))
    [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (13, 2), (13, 3), (13, 4), (13, 5), (13, 6), (13, 7), (13, 8), (13, 9), (13, 10), (13, 11), (13, 12), (13, 13), (12, 13), (11, 13), (10, 13), (9, 13), (8, 13), (7, 13), (6, 13), (5, 13), (4, 13), (3, 13), (2, 13), (1, 13), (1, 12), (1, 11), (1, 10), (1, 9), (1, 8), (1, 7), (1, 6), (1, 5), (1, 4), (1, 3), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (11, 2), (12, 2), (12, 3), (12, 4), (12, 5), (12, 6), (12, 7), (12, 8), (12, 9), (12, 10), (12, 11), (12, 12), (11, 12), (10, 12), (9, 12), (8, 12), (7, 12), (6, 12), (5, 12), (4, 12), (3, 12), (2, 12), (2, 11), (2, 10), (2, 9), (2, 8), (2, 7), (2, 6), (2, 5), (2, 4), (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3), (11, 3), (11, 4), (11, 5), (11, 6), (11, 7), (11, 8), (11, 9), (11, 10), (11, 11), (10, 11), (9, 11), (8, 11), (7, 11), (6, 11), (5, 11), (4, 11), (3, 11), (3, 10), (3, 9), (3, 8), (3, 7), (3, 6), (3, 5), (3, 4), (4, 4), (5, 4), (6, 4), (7, 4), (8, 4), (9, 4), (10, 4), (10, 5), (10, 6), (10, 7), (10, 8), (10, 9), (10, 10), (9, 10), (8, 10), (7, 10), (6, 10), (5, 10), (4, 10), (4, 9), (4, 8), (4, 7), (4, 6), (4, 5)]
    """
    if left == 5:
        return []
    else:
        return chain(map(lambda x: (x, top),    range(left, right+1)),
                     map(lambda y: (right, y),  range(top+1, bottom+1)),
                     map(lambda x: (x, bottom), range(right-1, left-1, -1)),
                     map(lambda y: (left, y),   range(bottom-1, top, -1)),
                     spiral(left+1, right-1, top+1, bottom-1))

class GameState:
    def __init__(self, struct):
        self.turn    = struct['turn']
        self.walls   = set([(pt[0], pt[1]) for pt in struct['walls']])
        self.blocks  = set([(pt[0], pt[1]) for pt in struct['blocks']])
        self.players = struct['players']
        self.bombs   = struct['bombs']
        self.items   = struct['items']
        self.fires   = set([(pt[0], pt[1]) for pt in struct['fires']])

    def copy(self):
        global copy
        return copy.deepcopy(self)

    def transition(self, id_to_move):
        state = self.copy()
        state.transition_unsafe(id_to_move)
        return state

    def find_player(self, id):
        """id が id のプレーヤーを取得する。

        >>> GameState(TEST_DATA).find_player(1)['name'] == 'よてぱい'
        True
        """
        return [p for p in self.players if p['id'] == id][0]

    def isblock(self, pos):
        """pos がブロックであるか。

        >>> GameState(TEST_DATA).isblock(to_pos((3, 2)))
        True
        >>> GameState(TEST_DATA).isblock(to_pos((2, 2)))
        False
        """
        return to_coords(pos) in self.blocks

    def isitem(self, pos):
        return len([i for i in self.items if i['pos'] == pos]) > 0

    def iswall(self, pos):
        """pos が壁であるか。

        >>> GameState(TEST_DATA).iswall(to_pos((0, 0)))
        True
        >>> GameState(TEST_DATA).iswall(to_pos((1, 1)))
        False
        """
        return to_coords(pos) in self.walls

    def explode_bomb(self, bomb):
        def fire_column(pos, dirvec, power):
            if power == 0:
                return []
            else:
                next_pos = addvec(pos, dirvec)
                if self.iswall(next_pos):
                    return []
                elif self.isblock(next_pos) or self.isitem(next_pos):
                    return [to_coords(next_pos)]
                else:
                    return [to_coords(next_pos)] + \
                        fire_column(next_pos, dirvec, power - 1)

        cols = chain(*map(lambda d: fire_column(bomb['pos'],
                                                d,
                                                bomb['power']),
                          [[0, -1], [0, 1], [-1, 0], [1, 0]]))
        return list(cols) + [to_coords(bomb['pos'])]

    def explode_bombs(self, bs):
        return list(chain(*map(lambda b: self.explode_bomb(b), bs)))

    def item_effect_unsafe(self, item, player):
        if item['name'] == '力':
            player['power'] += 1
        elif item['name'] == '弾':
            player['setBombLimit'] += 1
        else:
            raise

    def transition_unsafe(self, id_to_move):
        for id, move in sorted(id_to_move, key = lambda p: p[0]):
            self.eval_put_bomb_action_unsafe(self.find_player(id), move)

        for id, move in sorted(id_to_move, key = lambda p: p[0]):
            self.eval_move_action_unsafe(self.find_player(id), move)

        self.turn += 1

        if self.turn >= 360 and self.turn - 360 < len(GameState.FALLING_WALLS):
            pt = GameState.FALLING_WALLS[self.turn-360]
            self.walls |= {pt}
            self.blocks -= {pt}
            self.items = [i for i in self.items if to_coords(i['pos']) != pt]
            self.bombs = [b for b in self.bombs if to_coords(b['pos']) != pt]

        for bomb in self.bombs:
            bomb['timer'] -= 1

        for p in self.players:
          for i in self.items:
              if i['pos'] == p['pos']:
                  self.item_effect_unsafe(i, p)
                  self.items = [j for j in self.items if j != i]

        bombs_to_explode = [b for b in self.bombs if b['timer'] <= 0]
        new_fires = set()
        while bombs_to_explode:
            new_fires |= set(self.explode_bombs(bombs_to_explode))
            self.bombs = [b for b in self.bombs if not b in bombs_to_explode]
            bombs_to_explode = [b for b in self.bombs if to_coords(b['pos']) in new_fires]
        self.fires = new_fires

        self.items = [i for i in self.items if not to_coords(i['pos']) in self.fires]

        for coords in [pt for pt in self.blocks if pt in self.fires]:
            if random.random() < 20.0/90:
                if random.random() < 0.5:
                    name = '力'
                else:
                    name = '弾'
                self.items.append({ 'pos': to_pos(coords), 'name': name})
            self.blocks.remove(coords)

        def isdead(player):
            coords = to_coords(player['pos'])
            return coords in self.fires or coords in self.walls

        for player in [p for p in self.players if isdead(p)]:
            player['isAlive'] = False
            player['ch'] = '墓'

        return self

    def player_can_set_bomb(self, player):
        return player['isAlive'] and \
               not self.isbomb(player['pos']) and \
               player['setBombLimit'] > player['setBombCount']

    def isbomb(self, pos):
        return len([b for b in self.bombs if b['pos'] == pos]) > 0

    def player_set_bomb_unsafe(self, player):
        player['setBombCount'] += 1
        player['totalSetBombCount'] += 1
        self.bombs += [{'pos': player['pos'],
                        'timer': 10,
                        'power': player['power']}]

    DIR_OFFSETS = {
        'UP'    : [ 0, -1],
        'DOWN'  : [ 0,  1],
        'LEFT'  : [-1,  0],
        'RIGHT' : [ 1,  0],
        'STAY'  : [ 0,  0]
    }

    def eval_put_bomb_action_unsafe(self, player, move):
        if move.bomb and self.player_can_set_bomb(player):
            self.player_set_bomb_unsafe(player)

    def eval_move_action_unsafe(self, player, move):
        next_pos = addvec(player['pos'], GameState.DIR_OFFSETS[move.command])

        if player['isAlive'] and self.isenterable(next_pos):
            player['pos'] = next_pos

    FALLING_WALLS = list(spiral(1, 13, 1, 13))

    def isfinished(self):
        return len([p for p in self.players if p['isAlive']]) <= 1

    def winner(self):
        if not self.isfinished():
            return None
        else:
            return [p for p in self.players if p['isAlive']][0]

    def isenterable(self, pos):
        return not (self.iswall(pos) or self.isblock(pos) or self.isbomb(pos))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
