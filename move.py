class Move:
    def __init__(self, command, bomb, comment = ""):
        if not isinstance(bomb, bool):
            raise
        self.command = command
        self.bomb = bomb
        self.comment = comment

    def __repr__(self):
        return "({0},{1},{2})".format(self.command, self.bomb, self.comment)

    def __str__(self):
        return "{0},{1},{2}".format(self.command, self.bomb, self.comment)

if __name__ == "__main__":
    m = Move("STAY", False)
    print(m)
