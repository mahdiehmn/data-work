import os
import pygambit as gbt


def find_dominated_strategies(matrix):
    """
    Identify dominated strategies in a 3x3 matrix.

    :param matrix: A 3x3x2 matrix (list of lists of tuples) representing payoffs.
    :return: A dictionary with dominated rows and columns.
    """
    dominated = {"rows": [], "cols": []}

    for i in range(3):
        for j in range(3):
            if i != j:  # rows are compared with rows so we don't want repeated comparisons.
                if all(matrix[i][k][0] <= matrix[j][k][0] for k in range(3)) and any(
                    matrix[i][k][0] < matrix[j][k][0] for k in range(3)
                ):
                    dominated["rows"].append((i, j))

    for i in range(3):
        for j in range(3):
            if i != j:
                if all(matrix[k][i][1] <= matrix[k][j][1] for k in range(3)) and any(
                    matrix[k][i][1] < matrix[k][j][1] for k in range(3)
                ):
                    dominated["cols"].append((i, j))

    return dominated


def load_games(matrices_folder):
    """
    Load all .nfg games and convert them to payoff matrices.

    :param matrices_folder: Path to the folder containing .nfg files.
    :return: A list of 3x3x2 payoff matrices.
    """
    matrices = []
    for i in range(24):
        game_file = os.path.join(matrices_folder, f"filtered_{i}.nfg")
        game = gbt.Game.read_game(game_file)

        matrix = []
        for row in range(3):
            matrix_row = []
            for col in range(3):
                matrix_row.append(
                    (
                        int(game[row, col][game.players[0]]),
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

        dominated = find_dominated_strategies(matrix)

        if dominated["rows"]:
            for row_i, row_j in dominated["rows"]:
                print(f"  Row {row_i} is dominated by Row {row_j}")
        else:
            print("  No dominated rows.")

        if dominated["cols"]:
            for col_i, col_j in dominated["cols"]:
                print(f"  Column {col_i} is dominated by Column {col_j}")
        else:
            print("  No dominated columns.")
