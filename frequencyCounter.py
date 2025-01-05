import pickle


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


if __name__ == "__main__":
    choices_file = r'E:\data works\nse_data\ordered_filtered_120.pkl'
    frequencies = count_option_frequencies(choices_file)

    with open('frequencies.txt', 'w') as output:

        for game_id, counts in frequencies.items():
            output.write(
                f"Game {game_id}: Option 0 = {counts[0]}, Option 1 = {counts[1]}, Option 2 = {counts[2]}\n")
            print(
                f"Game {game_id}: Option 0 = {counts[0]}, Option 1 = {counts[1]}, Option 2 = {counts[2]}")

    print("Frequencies saved to frequencies.txt")
