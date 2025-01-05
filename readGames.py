import pickle
import pygambit as gbt
import numpy as np


class ReadGames:
    def __init__(self, game_file):
        self.game_file = game_file
        self.game = self._load_game()
        self.matrix = self._convert_game_to_np()

    def _load_game(self):
        return gbt.Game.read_game(self.game_file)

    def _convert_game_to_np(self):
        m = np.zeros(shape=(3, 3, 2))
        for i in range(3):
            for j in range(3):
                m[i][j][0] = self.game[i, j][self.game.players[0]]
                m[i][j][1] = self.game[i, j][self.game.players[1]]
        return m

    def game_to_string(self):
        s = ""
        for i in range(3):
            for j in range(3):
                s += f"({int(self.game[i, j][self.game.players[0]])}, {int(self.game[i, j][self.game.players[1]])}) "
            if i < 2:
                s += "\n"
        return s

    @staticmethod
    def read():  # type: ignore ->list[ReadGames]
        list = []
        for i in range(24):
            game_file = f"filtered_games/filtered_{i}.nfg"
            loader = ReadGames(game_file)
            list.append(loader)
        return list


def main():
    for i in range(24):
        game_file = f"filtered_games/filtered_{i}.nfg"
        loader = ReadGames(game_file)

        print(loader.game)
        print(loader.game_to_string())
        print()


if __name__ == "__main__":
    main()
