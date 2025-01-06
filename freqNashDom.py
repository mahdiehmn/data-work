import os
import pickle
import matplotlib.pyplot as plt
import nashpy as nash
import numpy as np
import pygambit as gbt


def find_nash_strategies(game_matrix):
    row_payoffs = np.array([[cell[0] for cell in row] for row in game_matrix])
    col_payoffs = np.array([[cell[1] for cell in row] for row in game_matrix])

    game = nash.Game(row_payoffs, col_payoffs)

    equilibria = game.support_enumeration()

    nash_strategies = set()
    pure_nash_equilibria = []
    for eq in equilibria:
        pure_eq = []
        for player, strategies in enumerate(eq):
            player_strategies = []
            for strategy, prob in enumerate(strategies):
                if prob == 1:
                    nash_strategies.add(strategy)
                    player_strategies.append(strategy)
            pure_eq.append(player_strategies)
        pure_nash_equilibria.append(pure_eq)

    return nash_strategies, pure_nash_equilibria


def find_dominated_strategies(matrix):
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


def load_game_matrix(game_file):
    game = gbt.Game.read_game(game_file)

    matrix = []
    for row in range(3):
        matrix_row = []
        for col in range(3):
            matrix_row.append(
                (
                    int(game[row, col][game.players[0]]),
                    int(game[row, col][game.players[1]])
                )
            )
        matrix.append(matrix_row)
    return matrix


def visualize_comparison(game_id, matrix, frequencies, dominated, nash_strategies, pure_nash_equilibria):
    options = [0, 1, 2]
    freq = frequencies[game_id]

    dominated_strategies = set(row[0] for row in dominated["rows"]) | set(
        col[0] for col in dominated["cols"])

    plt.figure(figsize=(14, 10))

    bar_colors = ['lightgreen'] * 3

    bars = plt.bar(options, freq, color=bar_colors,
                   alpha=0.6, label='Frequencies')

    for i in range(3):
        if i in dominated_strategies:
            bars[i].set_facecolor('red')

        if i in nash_strategies:
            plt.text(bars[i].get_x() + bars[i].get_width() / 2.0, bars[i].get_height() + 5, 'Nash',
                     ha='center', va='bottom', fontsize=10, color='black')

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{int(height)}',
                 ha='center', va='bottom', fontsize=10, color='black')

    # Set x-axis ticks explicitly to [0, 1, 2]
    plt.xticks(options, ['0', '1', '2'])

    plt.subplots_adjust(bottom=0.4)  # Increase bottom margin for text

    # Game Matrix text
    matrix_text = "\n".join(
        "  ".join(f"({cell[0]}, {cell[1]})" for cell in row) for row in matrix
    )
    plt.text(0.5, -0.2, f"Game {game_id} Matrix:\n{matrix_text}",
             fontsize=10, ha='center', va='top', transform=plt.gca().transAxes)

    # Dominated Strategies text
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
    plt.text(0.5, -0.4, f"Dominated Strategies:\n{dominated_text}",
             fontsize=10, ha='center', va='top', transform=plt.gca().transAxes)

    # Nash Equilibria text
    if pure_nash_equilibria:
        nash_text = "PNE:\n" + "\n".join(
            f"Row: {eq[0]}, Column: {eq[1]}" for eq in pure_nash_equilibria
        )
        plt.text(0.5, -0.6, nash_text, fontsize=10, ha='center',
                 va='top', transform=plt.gca().transAxes)

    # Adjust legend position
    plt.legend([
        plt.Rectangle((0, 0), 1, 1, color='lightgreen', alpha=0.6),
        plt.Rectangle((0, 0), 1, 1, color='red', alpha=0.6)
    ], ['Frequencies', 'Dominated Strategies'], loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=2)

    plt.title(
        f"Game {game_id}: Frequencies, Dominance, and Nash Equilibria", fontsize=14)
    plt.xlabel("Strategies (Options 0, 1, 2)", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.savefig(f"game_{game_id}_comparison.png", bbox_inches='tight')
    plt.close()


def main():
    matrices_folder = r"E:\\data works\\nse_data\\filtered_games"
    choices_file = r"E:\\data works\\nse_data\\ordered_filtered_120.pkl"

    frequencies = count_option_frequencies(choices_file)

    for game_id in range(24):
        game_file = os.path.join(matrices_folder, f"filtered_{game_id}.nfg")
        matrix = load_game_matrix(game_file)
        dominated = find_dominated_strategies(matrix)
        nash_strategies, pure_nash_equilibria = find_nash_strategies(matrix)

        print(f"Game {game_id}: Nash Strategies = {sorted(nash_strategies)}")

        visualize_comparison(game_id, matrix, frequencies,
                             dominated, nash_strategies, pure_nash_equilibria)


if __name__ == "__main__":
    main()
