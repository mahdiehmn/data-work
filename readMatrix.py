import os
import pygambit as gbt


def load_games(matrices_folder):
    """
    Load all .nfg games and convert them to payoff matrices.

    :param matrices_folder: Path to the folder containing .nfg files.
    :return: A list of 3x3x2 payoff matrices.
    """
    matrices = []
    for i in range(24):  # Assuming 24 games
        game_file = os.path.join(matrices_folder, f"filtered_{i}.nfg")
        game = gbt.Game.read_game(game_file)

        # Convert pygambit game to a 3x3x2 payoff matrix
        matrix = []
        for row in range(3):
            matrix_row = []
            for col in range(3):
                matrix_row.append(
                    (
                        # Row player's payoff
                        int(game[row, col][game.players[0]]),
                        # Column player's payoff
                        int(game[row, col][game.players[1]]),
                    )
                )
            matrix.append(matrix_row)
        matrices.append(matrix)
    return matrices


def print_matrix(matrix):
    """
    Print a 3x3 payoff matrix in a readable format.
    """
    for row in matrix:
        print("  ".join(f"({r[0]}, {r[1]})" for r in row))


if __name__ == "__main__":
    matrices_folder = r"E:\data works\nse_data\filtered_games"
    matrices = load_games(matrices_folder)

    for game_id, matrix in enumerate(matrices):
        print(f"\nGame {game_id} Matrix:")
        print_matrix(matrix)
