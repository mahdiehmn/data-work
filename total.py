import os
import pickle
import matplotlib.pyplot as plt
import pygambit as gbt
import numpy as np
import nashpy as nash


def find_nash_strategies(matrix):
    row_payoffs = np.array([[cell[0] for cell in row] for row in matrix])
    col_payoffs = np.array([[cell[1] for cell in row] for row in matrix])

    game = nash.Game(row_payoffs, col_payoffs)
    equilibria = game.support_enumeration()

    nash_strategies = set()
    for eq in equilibria:
        for player, strategies in enumerate(eq):
            for strategy, prob in enumerate(strategies):
                if prob == 1:
                    nash_strategies.add(strategy)

    return nash_strategies


def find_dominated_strategies(matrix):
    dominated = {"rows": [], "cols": []}
    for i in range(3):
        for j in range(3):
            if i != j:
                if all(matrix[i][k][0] <= matrix[j][k][0] for k in range(3)) and any(
                    matrix[i][k][0] < matrix[j][k][0] for k in range(3)
                ):
                    dominated["rows"].append(i)
    for i in range(3):
        for j in range(3):
            if i != j:
                if all(matrix[k][i][1] <= matrix[k][j][1] for k in range(3)) and any(
                    matrix[k][i][1] < matrix[k][j][1] for k in range(3)
                ):
                    dominated["cols"].append(i)
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


def plot_strategy_frequencies(frequencies):
    total_frequencies = [0, 0, 0]
    for game_id in frequencies:
        for strategy, count in enumerate(frequencies[game_id]):
            total_frequencies[strategy] += count
    options = [0, 1, 2]
    plt.figure(figsize=(10, 8))
    bars = plt.bar(
        options, total_frequencies, color=["blue", "green", "orange"], alpha=0.7
    )
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{int(height)}",
            ha="center",
            va="bottom",
            fontsize=10,
        )
    plt.title("Frequency of Play for Each Strategy Across All Games", fontsize=14)
    plt.xlabel("Strategies (0, 1, 2)", fontsize=12)
    plt.ylabel("Total Frequency", fontsize=12)
    plt.xticks(options)
    plt.savefig("total_strategy_frequencies.png", bbox_inches="tight")
    plt.close()


def plot_dominated_strategy_frequencies(matrices_folder):
    total_dominated = [0, 0, 0]
    matrices = load_games(matrices_folder)
    for matrix in matrices:
        dominated = find_dominated_strategies(matrix)
        for row in dominated["rows"]:
            total_dominated[row] += 1
        for col in dominated["cols"]:
            total_dominated[col] += 1
    options = [0, 1, 2]
    plt.figure(figsize=(10, 8))
    bars = plt.bar(
        options, total_dominated, color=["red", "purple", "yellow"], alpha=0.7
    )
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{int(height)}",
            ha="center",
            va="bottom",
            fontsize=10,
        )
    plt.title("Frequency of Dominated Strategies Across All Games", fontsize=14)
    plt.xlabel("Strategies (0, 1, 2)", fontsize=12)
    plt.ylabel("Total Frequency of Being Dominated", fontsize=12)
    plt.xticks(options)
    plt.savefig("total_dominated_strategy_frequencies.png",
                bbox_inches="tight")
    plt.close()


def plot_nash_strategy_frequencies(matrices_folder):
    total_nash = [0, 0, 0]
    matrices = load_games(matrices_folder)
    for matrix in matrices:
        nash_strategies = find_nash_strategies(matrix)
        for strategy in nash_strategies:
            total_nash[strategy] += 1
    options = [0, 1, 2]
    plt.figure(figsize=(10, 8))
    bars = plt.bar(
        options, total_nash, color=["cyan", "magenta", "lime"], alpha=0.7
    )
    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2.0,
            height,
            f"{int(height)}",
            ha="center",
            va="bottom",
            fontsize=10,
        )
    plt.title("Frequency of Nash Strategies Across All Games", fontsize=14)
    plt.xlabel("Strategies (0, 1, 2)", fontsize=12)
    plt.ylabel("Total Frequency of Being Nash", fontsize=12)
    plt.xticks(options)
    plt.savefig("total_nash_strategy_frequencies.png", bbox_inches="tight")
    plt.close()


def main():
    matrices_folder = r"E:\\data works\\nse_data\\filtered_games"
    choices_file = r"E:\\data works\\nse_data\\ordered_filtered_120.pkl"
    frequencies = count_option_frequencies(choices_file)
    plot_strategy_frequencies(frequencies)
    plot_dominated_strategy_frequencies(matrices_folder)
    plot_nash_strategy_frequencies(matrices_folder)


if __name__ == "__main__":
    main()
