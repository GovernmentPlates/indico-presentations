import os
import subprocess
from datetime import datetime
from collections import OrderedDict
import matplotlib.pyplot as plt
from aquarel import load_theme



REPO_PATH = "/home/troun/dev/indico"
TEST_SUFFIX = "_test.py"


def run_git(args):
    """Run a git command in the repo and return stdout."""
    return subprocess.check_output(["git", "-C", REPO_PATH] + args, text=True).strip()


def get_yearly_commits():
    """Get the last commit of each year."""
    log = run_git(["log", "--reverse", "--pretty=format:%H %ct"])
    commits = [line.split() for line in log.splitlines()]
    years = {}
    for commit_hash, timestamp in commits:
        year = datetime.utcfromtimestamp(int(timestamp)).year
        years[year] = commit_hash  # Keep latest per year
    return OrderedDict(sorted(years.items()))


def list_py_files(commit):
    """List all Python files in a commit tree."""
    tree = run_git(["ls-tree", "-r", "--name-only", commit])
    return [f for f in tree.splitlines() if f.endswith(".py")]


def read_file_from_commit(commit, filepath):
    """Get file contents from a commit without checking it out."""
    try:
        return run_git(["show", f"{commit}:{filepath}"])
    except subprocess.CalledProcessError:
        return ""  # Binary or unreadable file


def count_lines_in_commit(commit):
    """Count test and app lines in a commit."""
    test_lines = 0
    app_lines = 0
    for file in list_py_files(commit):
        content = read_file_from_commit(commit, file)
        line_count = len(content.splitlines())
        if file.endswith(TEST_SUFFIX):
            test_lines += line_count
        else:
            app_lines += line_count
    return test_lines, app_lines


def analyze_test_ratio():
    yearly_commits = get_yearly_commits()
    ratios = {}
    for year, commit in yearly_commits.items():
        print(f"Analyzing {year} ({commit})...")
        test, app = count_lines_in_commit(commit)
        total = test + app
        ratio = test / total if total > 0 else 0
        ratios[year] = ratio
        print(f"  {test} test lines, {app} app lines -> ratio = {ratio:.2f}")
    return ratios


def plot_ratios(ratios):
    years = list(ratios.keys())
    values = list(ratios.values())
    plt.figure(figsize=(10, 5))
    plt.plot(years, values, marker="o", linestyle="-", color="purple")
    plt.title("Test Code Ratio Over Time")
    plt.xlabel("Year")
    plt.ylabel("Test Code Ratio")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("../assets/slides/stats/test_ratio.png", dpi=300)
    plt.show()


if __name__ == "__main__":
    with load_theme("gruvbox_dark"):
        ratios = analyze_test_ratio()
        plot_ratios(ratios)
