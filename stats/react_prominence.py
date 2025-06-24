from matplotlib import pyplot as plt
from aquarel import load_theme
import matplotlib.dates as mdates
import datetime

formatter = mdates.DateFormatter("%Y") ### formatter of the date
locator = mdates.YearLocator()

data = [
    (datetime.datetime.strptime("2018-03-07", "%Y-%m-%d"), 0.0, 236380.0),
    (datetime.datetime.strptime("2018-06-01", "%Y-%m-%d"), 4415.0, 231769.0),
    (datetime.datetime.strptime("2018-10-26", "%Y-%m-%d"), 11531.0, 244230.0),
    (datetime.datetime.strptime("2019-02-27", "%Y-%m-%d"), 17931.0, 257019.0),
    (datetime.datetime.strptime("2019-07-18", "%Y-%m-%d"), 22523.0, 258741.0),
    (datetime.datetime.strptime("2020-02-04", "%Y-%m-%d"), 28359.0, 274280.0),
    (datetime.datetime.strptime("2020-08-19", "%Y-%m-%d"), 33855.0, 299473.0),
    (datetime.datetime.strptime("2021-03-18", "%Y-%m-%d"), 35036.0, 297446.0),
    (datetime.datetime.strptime("2021-07-01", "%Y-%m-%d"), 36781.0, 330005.0),
    (datetime.datetime.strptime("2021-11-16", "%Y-%m-%d"), 40275.0, 334776.0),
    (datetime.datetime.strptime("2022-03-29", "%Y-%m-%d"), 37902.0, 331865.0),
    (datetime.datetime.strptime("2022-11-30", "%Y-%m-%d"), 48033.0, 346714.0),
    (datetime.datetime.strptime("2023-08-17", "%Y-%m-%d"), 49853.0, 333041.0),
    (datetime.datetime.strptime("2023-11-27", "%Y-%m-%d"), 51900.0, 340186.0),
    (datetime.datetime.strptime("2024-02-27", "%Y-%m-%d"), 54626.0, 341839.0),
    (datetime.datetime.strptime("2024-04-25", "%Y-%m-%d"), 55535.0, 346286.0),
    (datetime.datetime.strptime("2024-08-12", "%Y-%m-%d"), 55653.0, 347154.0),
    (datetime.datetime.strptime("2024-10-09", "%Y-%m-%d"), 57529.0, 357523.0),
    (datetime.datetime.strptime("2025-01-17", "%Y-%m-%d"), 57224.0, 356503.0),
    (datetime.datetime.strptime("2025-06-04", "%Y-%m-%d"), 57734.0, 359037.0),
    (datetime.datetime.strptime("2025-06-17", "%Y-%m-%d"), 58002.0, 360375.0),
]


def plot_react_prominence(data):
    dates, react_lines, total_lines = zip(*data)

    plt.figure(figsize=(12, 6))
    plt.gca().xaxis.set_major_formatter(formatter) ## calling the formatter for the x-axis
    plt.gca().xaxis.set_major_locator(locator)
    plt.plot(dates, react_lines, marker="o", linestyle="-", color="teal")
    plt.title("React Use Over Time")
    # plt.xlabel("Date")
    plt.ylabel("Lines of code")
    plt.xticks(rotation=45)
    # Create acustom y ticks that shows bothe the absolute number of lines and the percentage of React lines
    y_ticks = [0, 10000, 20000, 30000, 40000, 50000, 60000]
    y_labels = [f"{tick} ({tick / total_lines[-1] * 100:.1f}%)" for tick in y_ticks]
    plt.yticks(y_ticks, y_labels)

    plt.grid(True)
    plt.tight_layout()
    plt.savefig("../assets/slides/react/react_use.png")
    plt.show()


def main():
    plot_react_prominence(data)


if __name__ == "__main__":
    with load_theme("gruvbox_dark"):
        main()
