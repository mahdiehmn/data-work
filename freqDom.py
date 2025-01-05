import os
import pickle
import matplotlib.pyplot as plt
import pygambit as gbt


def find_dominated_strategies(matrix):
    """
    Identify dominated strategies in a 3x3 matrix.

    :param matrix: A 3x3x2 matrix (list of lists of tuples) representing payoffs.
    :return: A dictionary with dominated rows and columns as tuples (dominated, dominating).
    """
    dominated = {"rows": [], "cols": []}

    for i in range(3):
        for j in range(3):
            if i != j:
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


def count_option_frequencies(choices_file):
    with open(choices_file, "rb") as f:
        data = pickle.load(f)

    num_games = data.shape[1]
    frequencies = {game: [0, 0, 0] for game in range(num_games)}

    for player_id in range(data.shape[0]):
        for game_id in range(data.shape[1]):
            for option in range(data.shape[2]):
                if data[player_id, game_id, option] == 1:
                    frequencies[game_id][option] += 1

    return frequencies


def load_games(matrices_folder):
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


def visualize_comparison(game_id, matrix, frequencies, dominated):
    """
    Visualize the comparison of strategy frequencies and dominated strategies for a specific game,
    including the game matrix and dominated strategy details.
    """
    options = [0, 1, 2]
    freq = frequencies[game_id]

    dominated_strategies = set(row[0] for row in dominated["rows"]) | set(
        col[0] for col in dominated["cols"])

    print(f"\nGame {game_id} Matrix:")
    for row in matrix:
        print("  " + "  ".join(f"({r[0]}, {r[1]})" for r in row))
    print("\nDominated Strategies:")
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

    plt.figure(figsize=(10, 7))

    bar_colors = ['lightgreen', 'lightgreen', 'lightgreen']

    bars = plt.bar(options, freq, color=bar_colors,
                   alpha=0.6, label='Frequencies')

    for i in dominated_strategies:
        plt.bar(i, freq[i], color='red', alpha=0.6, label='Dominated Strategy')

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{int(height)}',
                 ha='center', va='bottom', fontsize=10, color='black')

    plt.yticks(range(0, max(freq) + 1, 10))

    plt.xticks(options, ['0', '1', '2'])

    matrix_text = "\n".join(
        "  ".join(f"({cell[0]}, {cell[1]})" for cell in row) for row in matrix
    )
    plt.text(0.5, -0.3, f"Game {game_id} Matrix:\n{matrix_text}",
             fontsize=10, ha='center', va='top', transform=plt.gca().transAxes)

    dominated_text = []
    if dominated["rows"]:
        dominated_text.append(
            "\n".join(
                f"Row {row_i} is dominated by Row {row_j}" for row_i, row_j in dominated["rows"])
        )
    else:
        dominated_text.append("No dominated rows.")
    if dominated["cols"]:
        dominated_text.append(
            "\n".join(
                f"Column {col_i} is dominated by Column {col_j}" for col_i, col_j in dominated["cols"])
        )
    else:
        dominated_text.append("No dominated columns.")

    dominated_text = "\n".join(dominated_text)
    plt.text(0.5, -0.7, f"Dominated Strategies:\n{dominated_text}",
             fontsize=10, ha='center', va='top', transform=plt.gca().transAxes)

    plt.title(
        f"Game {game_id}: Frequencies vs Dominated Strategies", fontsize=14)
    plt.xlabel("Strategies (Options 0, 1, 2)", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())

    plt.savefig(f"game_{game_id}_comparison.png", bbox_inches='tight')
    plt.close()


if __name__ == "__main__":
    matrices_folder = r"E:\data works\nse_data\filtered_games"
    choices_file = r"E:\data works\nse_data\ordered_filtered_120.pkl"

    matrices = load_games(matrices_folder)
    frequencies = count_option_frequencies(choices_file)

    for game_id, matrix in enumerate(matrices):
        dominated = find_dominated_strategies(matrix)
        visualize_comparison(game_id, matrix, frequencies, dominated)
