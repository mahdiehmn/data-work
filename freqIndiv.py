import os
import pickle
import matplotlib.pyplot as plt


def load_individual_choices(choices_file):
    with open(choices_file, "rb") as f:
        data = pickle.load(f)
    return data


def plot_individual_choices(data, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for individual_id in range(data.shape[0]):
        frequencies = [0, 0, 0]

        for game_id in range(data.shape[1]):
            for option in range(data.shape[2]):
                if data[individual_id, game_id, option] == 1:
                    frequencies[option] += 1

        options = [0, 1, 2]

        plt.figure(figsize=(8, 6))
        bars = plt.bar(
            options, frequencies, color=["blue", "green", "orange"], alpha=0.7
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

        plt.title(f"Individual {individual_id} Choices", fontsize=14)
        plt.xlabel("Strategies (0, 1, 2)", fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.xticks(options)

        file_name = os.path.join(
            output_folder, f"individual_{individual_id}.png")
        plt.savefig(file_name, bbox_inches="tight")
        plt.close()


def main():
    choices_file = r"E:\\data works\\nse_data\\ordered_filtered_120.pkl"
    output_folder = r"E:\\data works\\nse_data\\individual_plots"

    data = load_individual_choices(choices_file)
    plot_individual_choices(data, output_folder)


if __name__ == "__main__":
    main()
