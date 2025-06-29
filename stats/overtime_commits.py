import os
import subprocess
from datetime import datetime, time
from collections import defaultdict
import matplotlib.pyplot as plt
import pytz
import matplotlib.ticker as ticker
import matplotlib
from aquarel import load_theme
import numpy as np

# Geneva timezone (handles CET/CEST automatically)
local_tz = pytz.timezone("Europe/Zurich")

# Working hours: 08:30 to 17:30
start_work = time(hour=8, minute=30)
end_work = time(hour=17, minute=45)


def run_git_log(repo_path):
    if not os.path.exists(repo_path):
        raise FileNotFoundError(f"The path '{repo_path}' does not exist.")

    cmd = ["git", "-C", repo_path, "log", "--pretty=format:%at"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Git log failed: {result.stderr}")

    return result.stdout.strip().split("\n")


def is_after_hours(local_dt):
    local_time = local_dt.time()
    return local_time < start_work or local_time > end_work
    # return local_time > end_work
    # return local_time < start_work


def count_after_hours_commits(timestamps):
    year_counts = defaultdict(int)
    hour_counts = defaultdict(int)

    for ts in timestamps:
        try:
            dt_utc = datetime.utcfromtimestamp(int(ts)).replace(tzinfo=pytz.utc)
            dt_local = dt_utc.astimezone(local_tz)
            year = dt_local.year
            hour = dt_local.hour
            hour_counts[hour] += 1

            if is_after_hours(dt_local):
                year_counts[year] += 1
        except Exception:
            continue

    return year_counts, hour_counts


def plot_after_hours_commits(year_counts, hour_counts):
    years = sorted(year_counts.keys())
    values = [year_counts[year] for year in years]

    max_commits = max(values)
    colors = plt.cm.autumn([1 - v / max_commits for v in values])

    fig, ax = plt.subplots(figsize=(16, 9))
    # Remove top and right spines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(False)
    # plt.bar(years, values, color="coral")
    ax.bar(years, values, color=colors)

    ax.set_title("After-hours Commits")
    # plt.xlabel("Year")
    ax.set_ylabel("Commits")

    # Only show integer years on the x-axis
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))
    ax.set_xticks(
        [
            2009,
            2010,
            2011,
            2012,
            2013,
            2014,
            2015,
            2016,
            2017,
            2018,
            2019,
            2020,
            2021,
            2022,
            2023,
            2024,
            2025,
        ]
    )

    # ========================================================================
    # ========================================================================

    ins = ax.inset_axes([0.4, 0.5, 0.8, 0.8], polar=True)

    N = 24
    bottom = 4
    max_height = 8

    max_hour_commits = max(hour_counts.values())
    for hour in hour_counts:
        hour_counts[hour] = hour_counts[hour] / max_hour_commits

    hour_counts = sorted(hour_counts.items(), key=lambda x: x[0])
    counts = [count for hour, count in hour_counts]

    theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
    # radii = max_height * np.random.rand(N)
    radii = [count * max_height for count in counts]
    width = (2 * np.pi) / N

    # ax = plt.subplot(111, polar=True)
    bars = ins.bar(theta, radii, width=width, bottom=bottom)

    # Use custom colors and opacity
    for r, bar in zip(radii, bars):
        bar.set_facecolor(plt.cm.jet(r / 10.0))
        bar.set_alpha(0.8)

    ins.set_xticks(theta, [f'{n}:00' for n in np.arange(0, 24, step=1)])
    ins.grid(True, alpha=0.3)
    ins.yaxis.set_ticklabels([])

    fig.tight_layout()
    plt.savefig("../assets/slides/stats/overtime_commits.png", dpi=300)
    print(matplotlib.colors.cnames["coral"])
    plt.show()


# ---------- USAGE ----------
if __name__ == "__main__":
    repo_path = "/home/tomas/dev/indico"  # Default path, can be overridden

    timestamps = run_git_log(repo_path)
    year_counts, hour_counts = count_after_hours_commits(timestamps)
    with load_theme("gruvbox_dark"):
        plot_after_hours_commits(year_counts, hour_counts)
