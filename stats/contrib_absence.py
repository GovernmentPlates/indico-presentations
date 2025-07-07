import os
import subprocess
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt
from aquarel import load_theme


def run_git_log(repo_path):
    if not os.path.exists(repo_path):
        raise FileNotFoundError(f"The path '{repo_path}' does not exist.")

    cmd = ["git", "-C", repo_path, "log", "master", "--pretty=format:%ae|%ct"]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Git log failed: {result.stderr}")

    return result.stdout.strip().split("\n")


def parse_commit_data(lines):
    yearly_data = defaultdict(lambda: defaultdict(int))  # {year: {author: count}}

    for line in lines:
        try:
            email, timestamp = line.split("|")
            year = datetime.fromtimestamp(int(timestamp)).year
            yearly_data[year][email] += 1
        except ValueError:
            continue  # skip malformed lines

    return yearly_data


def calculate_contributor_absence_factor(yearly_data):
    factor_by_year = {}
    for year, contributions in yearly_data.items():
        total_commits = sum(contributions.values())
        sorted_contribs = sorted(contributions.values(), reverse=True)

        running_sum = 0
        count = 0
        for contrib in sorted_contribs:
            running_sum += contrib
            count += 1
            if running_sum >= total_commits / 2:
                break

        factor_by_year[year] = count
    return factor_by_year


def plot_contributor_absence(factor_by_year):
    years = sorted(factor_by_year.keys())
    factors = [factor_by_year[year] for year in years]

    fig, ax = plt.subplots(figsize=(16, 9))
    plt.plot(years, factors, marker="o", linestyle="-", color="teal")
    plt.title("Bus Factor by Year")
    plt.xlabel("Year")
    plt.ylabel("# contributors with >50% of commits")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

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

    ax.set_yticks([0, 1, 2, 3])

    ax.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig("../assets/slides/stats/bus_factor.png", dpi=300)
    plt.show()


# ---------- USAGE ----------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Calculate Contributor Absence Factor using raw git CLI."
    )
    parser.add_argument("repo_path", help="Path to the local Git repository")

    args = parser.parse_args()
    log_lines = run_git_log(args.repo_path)
    yearly_commit_data = parse_commit_data(log_lines)
    caf_by_year = calculate_contributor_absence_factor(yearly_commit_data)
    with load_theme("gruvbox_dark"):
        plot_contributor_absence(caf_by_year)
