import os
import pickle
import matplotlib.pyplot as plt
import nashpy as nash
import numpy as np


def find_nash_strategies(game_matrix):
    """
    Parse Nash equilibria from a game matrix using NashPy for computation.

    :param game_matrix: A 3x3x2 matrix (list of lists of tuples).
    :return: A set of strategies involved in Nash equilibria.
    """
    # Extract payoffs for row and column players
    row_payoffs = np.array([[cell[0] for cell in row] for row in game_matrix])
    col_payoffs = np.array([[cell[1] for cell in row] for row in game_matrix])

    # Create a NashPy game
    game = nash.Game(row_payoffs, col_payoffs)

    # Compute Nash equilibria
    equilibria = game.support_enumeration()

    # Extract pure Nash strategies
    nash_strategies = set()
    for eq in equilibria:
        for player, strategies in enumerate(eq):
            for strategy, prob in enumerate(strategies):
                if prob == 1:  # Only include pure strategies
                    nash_strategies.add(strategy)

    return nash_strategies


def count_option_frequencies(choices_file):
    """
    Count the frequency of each option (0, 1, 2) for each game.

    :return: A dictionary where keys are game indices, and values are lists of frequencies [count_0, count_1, count_2].
    """
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


def visualize_frequencies_vs_nash(game_id, frequencies, nash_strategies):
    """
    Visualize the comparison of strategy frequencies and Nash strategies for a specific game.
    """
    options = [0, 1, 2]  # Strategy indices
    freq = frequencies[game_id]

    # Create a new figure
    plt.figure(figsize=(10, 7))

    # Set colors for strategies: Red for Nash, Blue for Non-Nash
    bar_colors = ['red' if i in nash_strategies else 'blue' for i in options]

    # Create a bar chart for frequencies
    bars = plt.bar(options, freq, color=bar_colors, alpha=0.7)

    # Add the exact frequency values above each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{int(height)}',
                 ha='center', va='bottom', fontsize=10, color='black')

    # Set labels, title, and legend
    plt.title(f"Game {game_id}: Frequencies vs Nash Strategies", fontsize=14)
    plt.xlabel("Strategies (Options 0, 1, 2)", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)

    # Add legend
    plt.legend([
        plt.Rectangle((0, 0), 1, 1, color='blue', alpha=0.7),
        plt.Rectangle((0, 0), 1, 1, color='red', alpha=0.7)
    ], ['Non-Nash Strategy', 'Nash Strategy'])

    # Save the figure with a unique filename
    plt.savefig(f"game_{game_id}_nash_vs_frequencies.png", bbox_inches='tight')
    plt.close()  # Close the figure to avoid overlap


def load_game_matrix(game_file):
    """
    Load a game matrix from an .nfg file and return it as a 3x3x2 matrix.

    :param game_file: Path to the .nfg file.
    :return: A 3x3 matrix of tuples [(row payoff, column payoff)].
    """
    import pygambit as gbt
    game = gbt.Game.read_game(game_file)

    matrix = []
    for row in range(3):
        matrix_row = []
        for col in range(3):
            matrix_row.append(
                (
                    # Row player's payoff
                    int(game[row, col][game.players[0]]),
                    # Column player's payoff
                    int(game[row, col][game.players[1]])
                )
            )
        matrix.append(matrix_row)
    return matrix


def main():
    matrices_folder = r"E:\\data works\\nse_data\\filtered_games"
    choices_file = r"E:\\data works\\nse_data\\ordered_filtered_120.pkl"

    # Load frequencies
    frequencies = count_option_frequencies(choices_file)

    # Compare for each game
    for game_id in range(24):
        game_file = os.path.join(matrices_folder, f"filtered_{game_id}.nfg")
        matrix = load_game_matrix(game_file)
        nash_strategies = find_nash_strategies(matrix)

        print(f"Game {game_id}: Nash Strategies = {sorted(nash_strategies)}")

        visualize_frequencies_vs_nash(game_id, frequencies, nash_strategies)


if __name__ == "__main__":
    main()
