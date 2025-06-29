import os
import subprocess
from collections import defaultdict
from datetime import datetime
import matplotlib.pyplot as plt


def run_git_log(repo_path):
    if not os.path.exists(repo_path):
        raise FileNotFoundError(f"The path '{repo_path}' does not exist.")

    cmd = ["git", "-C", repo_path, "log", "--pretty=format:%ae|%ct"]
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

    plt.figure(figsize=(10, 5))
    plt.plot(years, factors, marker="o", linestyle="-", color="teal")
    plt.title("Contributor Absence Factor by Year")
    plt.xlabel("Year")
    plt.ylabel("# Contributors for 50% of commits")
    plt.grid(True)
    plt.tight_layout()
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
    plot_contributor_absence(caf_by_year)
