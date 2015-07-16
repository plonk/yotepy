#!/usr/bin/env python3 -u
import sys
import json

from game_state import GameState
from ai import BombmanAi

class BombmanClient:
    def __init__(self, name):
        self.name = name

    def run(self):
        self.interact()

    def interact(self):
        self.id = self.handshake(self.name)
        self.ai = BombmanAi(self.name, self.id)

        while True:
            state = self.recv_game_state()
            if not state:
                break
            move = self.ai.move(state)
            sys.stdout.write(str(move) + "\n")

    def handshake(self, name):
        sys.stdout.write(name + "\n")
        line = sys.stdin.readline()
        return int(line)

    def recv_game_state(self):
        json_str = sys.stdin.readline()
        if json_str:
            return GameState(json.loads(json_str))
        else:
            return None

name = (len(sys.argv) >= 2 and sys.argv[1]) or "よてぱい"
BombmanClient(name).run()
