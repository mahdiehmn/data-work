import os
import numpy as np
import pygambit as gbt


def parse_and_save_games(input_folder, output_folder):
    """
    Parses all .nfg files in the input_folder using pygambit, prints the payoff matrices,
    and saves them as .npy files in the output_folder.

    Args:
        input_folder (str): Path to the folder containing .nfg files.
        output_folder (str): Path to the folder where .npy files will be saved.
    """
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # List all files in the input folder
    try:
        files = os.listdir(input_folder)
    except FileNotFoundError:
        print(f"Error: Input folder '{input_folder}' does not exist.")
        return

    # Filter for .nfg files (case-insensitive)
    nfg_files = [f for f in files if f.lower().endswith('.nfg')]

    if not nfg_files:
        print(f"No .nfg files found in '{input_folder}'.")
        return

    print(
        f"Found {len(nfg_files)} .nfg file(s) in '{input_folder}'. Processing...\n")

    for file_name in sorted(nfg_files):
        input_path = os.path.join(input_folder, file_name)
        base_name = os.path.splitext(file_name)[0]
        output_file = base_name + '.npy'
        output_path = os.path.join(output_folder, output_file)

        try:
            # Read the game using pygambit
            game = gbt.Game.read_game(input_path)

            # Check if the game has exactly 2 players
            num_players = len(game.players)
            if num_players != 2:
                print(
                    f"Skipping {file_name}: Only two-player games are supported.")
                continue

            # Retrieve the number of strategies for each player
            num_strategies_p1 = len(game.players[0].strategies)
            num_strategies_p2 = len(game.players[1].strategies)

            # Initialize a matrix to hold the payoffs
            # Shape: (num_strategies_p1, num_strategies_p2, 2)
            payoff_matrix = np.zeros((num_strategies_p1, num_strategies_p2, 2))

            for i in range(num_strategies_p1):
                for j in range(num_strategies_p2):
                    # Get the payoffs for the strategy pair (i, j)
                    profile = game[i, j]
                    payoff_p1 = float(profile[game.players[0]])
                    payoff_p2 = float(profile[game.players[1]])
                    payoff_matrix[i, j, 0] = payoff_p1
                    payoff_matrix[i, j, 1] = payoff_p2

            # Print the matrix for verification
            print(f"Combined Payoff Matrix for {file_name}:")
            print(payoff_matrix)
            print()

            # Save the matrix as a .npy file
            np.save(output_path, payoff_matrix)
            print(
                f"Successfully parsed and saved: {file_name} -> {output_file}\n")

        except Exception as e:
            print(f"Failed to parse {file_name}: {e}\n")


if __name__ == "__main__":
    # Define input and output folders
    input_folder = r"E:\PS-new_ideia (2)\PS-new_ideia\nse_data\filtered_games"
    output_folder = r"E:\PS-new_ideia (2)\PS-new_ideia\nse_data\parsed_games"

    parse_and_save_games(input_folder, output_folder)
